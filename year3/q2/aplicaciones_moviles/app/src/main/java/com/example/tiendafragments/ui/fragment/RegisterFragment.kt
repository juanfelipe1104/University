package com.example.tiendafragments.ui.fragment

import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.example.tiendafragments.R
import com.example.tiendafragments.databinding.FragmentRegisterBinding
import com.example.tiendafragments.model.User
import com.google.android.material.snackbar.Snackbar
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.database.FirebaseDatabase

class RegisterFragment : Fragment() {

    private lateinit var binding: FragmentRegisterBinding
    private lateinit var auth: FirebaseAuth
    private lateinit var database: FirebaseDatabase

    override fun onAttach(context: Context) {
        super.onAttach(context)

        auth = FirebaseAuth.getInstance()

        database =
            FirebaseDatabase.getInstance("https://tiendafragment-default-rtdb.europe-west1.firebasedatabase.app/")
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        binding = FragmentRegisterBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        actions()
    }

    private fun actions() {
        binding.buttonConfirmRegister.setOnClickListener {
            val mail = binding.editTextEmailRegister.text.toString().trim()
            val password = binding.editTextPasswordRegister.text.toString().trim()
            val name = binding.editTextName.text.toString().trim()
            val surname = binding.editTextLastName.text.toString().trim()

            if (mail.isBlank() || password.isBlank() || name.isBlank() || surname.isBlank()) {
                Snackbar.make(binding.root, "Completa todos los campos", Snackbar.LENGTH_LONG).show()
                return@setOnClickListener
            }
            if (password.length < 6) {
                Snackbar.make(binding.root, "La contraseña debe tener al menos 6 caracteres", Snackbar.LENGTH_LONG).show()
                return@setOnClickListener
            }
            binding.buttonConfirmRegister.isEnabled = false

            auth.createUserWithEmailAndPassword(mail, password)
                .addOnCompleteListener { task ->
                    if (task.isSuccessful) {
                        val firebaseUser = auth.currentUser

                        if (firebaseUser != null) {
                            val uid = firebaseUser.uid

                            val user = User(uid, mail, name, surname)

                            database.reference
                                .child("users")
                                .child(uid)
                                .setValue(user)
                                .addOnSuccessListener {
                                    Snackbar.make(
                                        binding.root,
                                        "Registro completado",
                                        Snackbar.LENGTH_LONG
                                    ).show()

                                    findNavController().navigate(
                                        R.id.action_registerFragment_to_mainFragment
                                    )
                                }
                                .addOnFailureListener {
                                    binding.buttonConfirmRegister.isEnabled = true
                                    Snackbar.make(
                                        binding.root,
                                        "Usuario creado, pero falló al guardar en la base de datos",
                                        Snackbar.LENGTH_LONG
                                    ).show()
                                }
                        }
                    } else {
                        binding.buttonConfirmRegister.isEnabled = true
                        Snackbar.make(
                            binding.root,
                            "Fallo en el registro: ${task.exception?.message}",
                            Snackbar.LENGTH_LONG
                        ).show()
                    }
                }
        }
    }
}
