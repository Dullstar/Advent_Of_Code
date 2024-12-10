module dict;

import std.typecons;

// thin wrapper around the built-in associative array to make it a little less annoying
// for now I'm keeping it fairly minimal and only adding features as I need/want them
struct Dict(K, V)
{
    NullableRef!V opIndex(K key)
    {
        V* ptr = key in data;
        if (ptr is null) return NullableRef!V();
        else return NullableRef!V(ptr);
    }
    void opIndexAssign(V value, K key)
    {
        data[key] = value;
    }
    V[K] data; 
}