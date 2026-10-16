package se.korkort

/** Resource integrity uses the same SHA-256 identity as the approved build-time bindings. */
internal fun assetSha256(input: ByteArray): Sha256 {
    val k=intArrayOf(0x428a2f98,0x71374491,0xb5c0fbcf.toInt(),0xe9b5dba5.toInt(),0x3956c25b,0x59f111f1,0x923f82a4.toInt(),0xab1c5ed5.toInt(),0xd807aa98.toInt(),0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe.toInt(),0x9bdc06a7.toInt(),0xc19bf174.toInt(),0xe49b69c1.toInt(),0xefbe4786.toInt(),0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152.toInt(),0xa831c66d.toInt(),0xb00327c8.toInt(),0xbf597fc7.toInt(),0xc6e00bf3.toInt(),0xd5a79147.toInt(),0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e.toInt(),0x92722c85.toInt(),0xa2bfe8a1.toInt(),0xa81a664b.toInt(),0xc24b8b70.toInt(),0xc76c51a3.toInt(),0xd192e819.toInt(),0xd6990624.toInt(),0xf40e3585.toInt(),0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814.toInt(),0x8cc70208.toInt(),0x90befffa.toInt(),0xa4506ceb.toInt(),0xbef9a3f7.toInt(),0xc67178f2.toInt())
    val h=intArrayOf(0x6a09e667,0xbb67ae85.toInt(),0x3c6ef372,0xa54ff53a.toInt(),0x510e527f,0x9b05688c.toInt(),0x1f83d9ab,0x5be0cd19)
    val data=ByteArray(((input.size+9+63)/64)*64);input.copyInto(data);data[input.size]=0x80.toByte()
    val bits=input.size.toLong()*8L
    repeat(8) { data[data.lastIndex-it]=(bits ushr (it*8)).toByte() }
    fun rr(v:Int,n:Int)=(v ushr n) or (v shl (32-n))
    for(start in data.indices step 64) {
        val w=IntArray(64)
        repeat(16) { n -> repeat(4) { b -> w[n]=(w[n] shl 8) or (data[start+n*4+b].toInt() and 255) } }
        for(n in 16..63) {
            val a=w[n-15];val b=w[n-2]
            w[n]=w[n-16]+(rr(a,7) xor rr(a,18) xor (a ushr 3))+w[n-7]+(rr(b,17) xor rr(b,19) xor (b ushr 10))
        }
        var a=h[0];var b=h[1];var c=h[2];var d=h[3];var e=h[4];var f=h[5];var g=h[6];var z=h[7]
        repeat(64) { n ->
            val t=z+(rr(e,6) xor rr(e,11) xor rr(e,25))+((e and f) xor (e.inv() and g))+k[n]+w[n]
            val u=(rr(a,2) xor rr(a,13) xor rr(a,22))+((a and b) xor (a and c) xor (b and c))
            z=g;g=f;f=e;e=d+t;d=c;c=b;b=a;a=t+u
        }
        val values=intArrayOf(a,b,c,d,e,f,g,z);repeat(8) { h[it]+=values[it] }
    }
    return Sha256(h.joinToString("") { it.toUInt().toString(16).padStart(8,'0') })
}
