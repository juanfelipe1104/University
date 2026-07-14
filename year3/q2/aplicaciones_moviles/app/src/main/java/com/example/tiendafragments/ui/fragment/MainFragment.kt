package com.example.tiendafragments.ui.fragment

import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.example.tiendafragments.R
import com.example.tiendafragments.databinding.FragmentMainBinding
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.FirebaseUser
import com.google.firebase.database.FirebaseDatabase

class MainFragment : Fragment() {
    private lateinit var binding: FragmentMainBinding
    private var user: FirebaseUser? = null
    private lateinit var database: FirebaseDatabase

    override fun onAttach(context: Context) {
        super.onAttach(context)
        user = FirebaseAuth.getInstance().currentUser
        database = FirebaseDatabase.getInstance("https://tiendafragment-default-rtdb.europe-west1.firebasedatabase.app/")
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        binding = FragmentMainBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onStart() {
        super.onStart()
        if (user == null) {
            findNavController().navigate(R.id.action_mainFragment_to_loginFragment)
            return
        }
        binding.textMain.text = "Bienvenido ${user?.email}"
        binding.buttonOpenCatalog.setOnClickListener {
            findNavController().navigate(R.id.action_mainFragment_to_productListFragment)
        }
        binding.buttonLogout.setOnClickListener {
            FirebaseAuth.getInstance().signOut()
            findNavController().navigate(R.id.action_mainFragment_to_loginFragment)
        }
    }

    override fun onDetach() {
        super.onDetach()
    }
}
