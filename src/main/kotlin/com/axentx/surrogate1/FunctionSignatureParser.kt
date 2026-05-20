package com.axentx.surrogate1

import java.util.*

class FunctionSignatureParser {
    fun parse(signature: String): FunctionSignature {
        val parts = signature.split(" ")
        val returnType = parts[0]
        val functionName = parts[1].substringBefore("(")
        val parameters = parts[1].substringAfter("(").substringBefore(")").split(",").map { it.trim() }
        return FunctionSignature(returnType, functionName, parameters)
    }
}

data class FunctionSignature(val returnType: String, val name: String, val parameters: List<String>)