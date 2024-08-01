package com.ecommerce.order

import com.fasterxml.jackson.annotation.JsonProperty
import java.math.BigDecimal
import java.time.LocalDateTime

data class OrderItem(val productId: String, val quantity: Int, val price: BigDecimal)

class OrderProcessor {

    fun processUserOrder(
        @JsonProperty("userId") userId: String,
        @JsonProperty("orderItems") orderItems: List<OrderItem>,
        @JsonProperty("shippingAddress") shippingAddress: String,
        @JsonProperty("paymentMethod") paymentMethod: String
    ): OrderResult {
        // Validate order
        if (orderItems.isEmpty()) {
            return OrderResult(false, "Order must contain at least one item")
        }

        // Calculate total price
        val totalPrice = orderItems.sumOf { it.price * BigDecimal(it.quantity) }

        // Apply discount for orders over $100
        val finalPrice = if (totalPrice > BigDecimal(100)) {
            totalPrice * BigDecimal(0.9)  // 10% discount
        } else {
            totalPrice
        }

        // Simulate order processing
        Thread.sleep(1000)  // Pretend it takes a second to process

        // Generate order number
        val orderNumber = generateOrderNumber(userId)

        return OrderResult(
            success = true,
            message = "Order processed successfully",
            orderNumber = orderNumber,
            totalAmount = finalPrice,
            estimatedDelivery = LocalDateTime.now().plusDays(3)
        )
    }

    private fun generateOrderNumber(userId: String): String {
        return "ORD-${userId.take(5)}-${System.currentTimeMillis()}"
    }
}

data class OrderResult(
    val success: Boolean,
    val message: String,
    val orderNumber: String? = null,
    val totalAmount: BigDecimal? = null,
    val estimatedDelivery: LocalDateTime? = null
)