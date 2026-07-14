package com.example.tiendafragments.data

import com.example.tiendafragments.model.Product

object CartManager {
    private val products = mutableListOf<Product>()
    fun add(product: Product) { products.add(product) }
    fun clear() = products.clear()
    fun count(): Int = products.size
    fun total(): Double = products.sumOf(Product::price)
    fun isEmpty(): Boolean = products.isEmpty()
}
