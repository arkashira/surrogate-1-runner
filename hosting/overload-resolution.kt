package hosting

import java.util.*

class VersionedOverloadResolution {
    private val overloadMap = mutableMapOf<String, MutableList<Pair<String, String>>>()

    fun addOverload(version: String, functionName: String, overload: String) {
        val key = "$version:$functionName"
        if (!overloadMap.containsKey(key)) {
            overloadMap[key] = mutableListOf()
        }
        overloadMap[key]?.add(Pair(version, overload))
    }

    fun getOverloads(version: String, functionName: String): List<String> {
        val key = "$version:$functionName"
        return overloadMap.getOrDefault(key, mutableListOf()).map { it.second }
    }
}

fun main() {
    val resolution = VersionedOverloadResolution()
    resolution.addOverload("1.0", "foo", "foo(int)")
    resolution.addOverload("1.0", "foo", "foo(String)")
    resolution.addOverload("2.0", "foo", "foo(Double)")

    println(resolution.getOverloads("1.0", "foo")) // [foo(int), foo(String)]
    println(resolution.getOverloads("2.0", "foo")) // [foo(Double)]
}