package com.example.tiendafragments.ui.adapter

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.tiendafragments.R
import com.example.tiendafragments.databinding.ItemProductBinding
import com.example.tiendafragments.model.Product

class ProductAdapter(
    private val onDetails: (Product) -> Unit,
    private val onBuy: (Product) -> Unit
) : RecyclerView.Adapter<ProductAdapter.ProductViewHolder>() {
    private val products = mutableListOf<Product>()
    class ProductViewHolder(val binding: ItemProductBinding) : RecyclerView.ViewHolder(binding.root)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ProductViewHolder {
        val inflater = LayoutInflater.from(parent.context)
        return ProductViewHolder(ItemProductBinding.inflate(inflater, parent, false))
    }

    override fun onBindViewHolder(holder: ProductViewHolder, position: Int) {
        val product = products[position]
        with(holder.binding) {
            textProductTitle.text = product.title
            textProductPrice.text = root.context.getString(R.string.product_price, product.price)
            buttonDetails.setOnClickListener { onDetails(product) }
            buttonBuy.setOnClickListener { onBuy(product) }
            Glide.with(imageProduct).load(product.thumbnail)
                .placeholder(android.R.drawable.ic_menu_gallery)
                .error(android.R.drawable.ic_menu_report_image).into(imageProduct)
        }
    }

    override fun getItemCount(): Int = products.size

    fun submitList(items: List<Product>) {
        products.clear()
        products.addAll(items)
        notifyDataSetChanged()
    }
}
