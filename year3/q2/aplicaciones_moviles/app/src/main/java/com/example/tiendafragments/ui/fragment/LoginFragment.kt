package com.example.tiendafragments.ui.fragment

import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.example.tiendafragments.R
import com.example.tiendafragments.databinding.FragmentLoginBinding
import com.google.android.material.snackbar.Snackbar
import com.google.firebase.auth.FirebaseAuth

class LoginFragment : Fragment() {
    private lateinit var binding: FragmentLoginBinding
    private lateinit var auth: FirebaseAuth

    override fun onAttach(context: Context) {
        super.onAttach(context)
        auth = FirebaseAuth.getInstance()
    }

    override fun onResume() {
        super.onResume()
        if(auth.currentUser != null){
            auth.signOut()
        }
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View {
        binding = FragmentLoginBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        actions()
    }

    override fun onDetach() {
        super.onDetach()
    }

    private fun actions() {
        binding.buttonRegister.setOnClickListener {
            findNavController().navigate(R.id.action_loginFragment_to_registerFragment)
        }

        binding.buttonLogin.setOnClickListener {
            val email = binding.editTextEmail.text.toString().trim()
            val password = binding.editTextPassword.text.toString()
            if (email.isBlank() || password.isBlank()) {
                Snackbar.make(binding.root, "Completa el correo y la contraseña", Snackbar.LENGTH_LONG).show()
                return@setOnClickListener
            }
            binding.buttonLogin.isEnabled = false
            binding.buttonRegister.isEnabled = false
            auth.signInWithEmailAndPassword(email, password).addOnCompleteListener {
                binding.buttonLogin.isEnabled = true
                binding.buttonRegister.isEnabled = true
                if (it.isSuccessful) {
                    findNavController().navigate(R.id.action_loginFragment_to_mainFragment)
                } else {
                    Snackbar.make(
                        binding.root,
                        it.exception?.localizedMessage ?: "Error en el proceso de login",
                        Snackbar.LENGTH_LONG
                    ).show()
                }
            }
        }
    }
}
