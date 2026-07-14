package com.example.tiendafragments.ui.fragment

import android.os.Build
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.bumptech.glide.Glide
import com.example.tiendafragments.R
import com.example.tiendafragments.databinding.FragmentProductDetailBinding
import com.example.tiendafragments.model.Product

class ProductDetailFragment : Fragment() {
    private var _binding: FragmentProductDetailBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, state: Bundle?): View {
        _binding = FragmentProductDetailBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, state: Bundle?) {
        val product = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            requireArguments().getSerializable("product", Product::class.java)
        } else {
            @Suppress("DEPRECATION") requireArguments().getSerializable("product") as? Product
        } ?: return
        binding.textDetailTitle.text = product.title
        binding.textDetailDescription.text = product.description
        binding.textDetailCategory.text = product.category
        binding.textDetailPrice.text = getString(R.string.product_price, product.price)
        Glide.with(binding.imageDetail).load(product.thumbnail).into(binding.imageDetail)
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
