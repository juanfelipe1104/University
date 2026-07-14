package com.example.tiendafragments.model

import java.io.Serializable

data class ProductResponse(val products: List<Product> = emptyList())

data class Product(
    val id: Long = 0,
    val title: String = "",
    val description: String = "",
    val category: String = "",
    val price: Double = 0.0,
    val thumbnail: String = ""
) : Serializable
