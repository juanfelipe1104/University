package com.example.tiendafragments.ui.fragment

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.AdapterView
import android.widget.ArrayAdapter
import androidx.core.os.bundleOf
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.LinearLayoutManager
import com.android.volley.toolbox.JsonArrayRequest
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import com.android.volley.RequestQueue
import com.example.tiendafragments.R
import com.example.tiendafragments.data.CartManager
import com.example.tiendafragments.databinding.FragmentProductListBinding
import com.example.tiendafragments.model.Product
import com.example.tiendafragments.model.ProductResponse
import com.example.tiendafragments.ui.adapter.ProductAdapter
import com.google.android.material.snackbar.Snackbar
import com.google.gson.Gson

class ProductListFragment : Fragment() {
    private var _binding: FragmentProductListBinding? = null
    private val binding get() = _binding!!
    private val allProducts = mutableListOf<Product>()
    private lateinit var productAdapter: ProductAdapter
    private lateinit var requestQueue: RequestQueue

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, state: Bundle?): View {
        _binding = FragmentProductListBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, state: Bundle?) {
        requestQueue = Volley.newRequestQueue(requireContext())
        productAdapter = ProductAdapter(
            onDetails = { product ->
                findNavController().navigate(
                    R.id.action_productListFragment_to_productDetailFragment,
                    bundleOf("product" to product)
                )
            },
            onBuy = { product ->
                CartManager.add(product)
                updateCart()
                Snackbar.make(binding.root, getString(R.string.added_to_cart, product.title), Snackbar.LENGTH_SHORT).show()
            }
        )
        binding.recyclerProducts.adapter = productAdapter
        binding.recyclerProducts.layoutManager = if (resources.configuration.orientation == 1) {
            LinearLayoutManager(requireContext())
        } else {
            GridLayoutManager(requireContext(), 2)
        }
        binding.buttonCompletePurchase.setOnClickListener { completePurchase() }
        updateCart()
        loadProducts()
        loadCategories()
    }

    private fun loadProducts() {
        showLoading(true)
        val request = JsonObjectRequest(PRODUCTS_URL, { response ->
            val result = Gson().fromJson(response.toString(), ProductResponse::class.java)
            allProducts.clear()
            allProducts.addAll(result.products)
            productAdapter.submitList(allProducts)
            binding.textEmpty.visibility = if (allProducts.isEmpty()) View.VISIBLE else View.GONE
            showLoading(false)
        }, { error ->
            showLoading(false)
            binding.textEmpty.visibility = View.VISIBLE
            binding.textEmpty.text = getString(R.string.catalog_load_error)
            Snackbar.make(binding.root, error.message ?: getString(R.string.network_error), Snackbar.LENGTH_LONG).show()
        })
        request.tag = this
        requestQueue.add(request)
    }

    private fun loadCategories() {
        val request = JsonArrayRequest(CATEGORIES_URL, { response ->
            val categories = mutableListOf(getString(R.string.all_categories))
            repeat(response.length()) { categories.add(response.getString(it)) }
            val adapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_item, categories)
            adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
            binding.spinnerCategories.adapter = adapter
            binding.spinnerCategories.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
                override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                    val selected = categories[position]
                    productAdapter.submitList(if (position == 0) allProducts else allProducts.filter {
                        it.category.equals(selected, true)
                    })
                }
                override fun onNothingSelected(parent: AdapterView<*>?) = Unit
            }
        }, { Snackbar.make(binding.root, R.string.category_load_error, Snackbar.LENGTH_LONG).show() })
        request.tag = this
        requestQueue.add(request)
    }

    private fun completePurchase() {
        if (CartManager.isEmpty()) {
            Snackbar.make(binding.root, R.string.empty_cart, Snackbar.LENGTH_LONG).show()
            return
        }
        Snackbar.make(binding.root, getString(R.string.purchase_complete, CartManager.total()), Snackbar.LENGTH_LONG).show()
        CartManager.clear()
        updateCart()
    }

    private fun updateCart() {
        binding.textCartTotal.text = getString(R.string.cart_total, CartManager.count(), CartManager.total())
    }

    private fun showLoading(loading: Boolean) {
        binding.progressProducts.visibility = if (loading) View.VISIBLE else View.GONE
        binding.recyclerProducts.visibility = if (loading) View.INVISIBLE else View.VISIBLE
    }

    override fun onDestroyView() {
        requestQueue.cancelAll(this)
        super.onDestroyView()
        _binding = null
    }

    companion object {
        private const val PRODUCTS_URL = "https://dummyjson.com/products"
        private const val CATEGORIES_URL = "https://dummyjson.com/products/category-list"
    }
}
