package com.axentx.surrogate1

import java.util.*

class OverloadResolver {
    private val overloadMap = mutableMapOf<String, MutableList<FunctionSignature>>()

    fun addFunctionSignature(signature: FunctionSignature) {
        val key = "${signature.name}-${signature.parameters.joinToString("-")}"
        if (!overloadMap.containsKey(key)) {
            overloadMap[key] = mutableListOf()
        }
        overloadMap[key]?.add(signature)
    }

    fun getUniqueIdentifier(signature: FunctionSignature): String {
        val key = "${signature.name}-${signature.parameters.joinToString("-")}"
        val functions = overloadMap[key] ?: throw IllegalArgumentException("No such function signature")
        return "${signature.name}-${functions.indexOf(signature)}"
    }
}