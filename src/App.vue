<template>
    <div>
        <span>Network Address: </span>
        <input type="text" id="input-name" v-model="inputNetAddr">

        <span>Prefix (Subnet Mask): </span>
        <select name="prefix" v-model="inputPrefix">
            <option v-for="x in 32" :value=x>/{{ x }} ({{ prefix_to_subnetmask(x) }})</option>
        </select>
        <button @click="handleValidate"> Validate </button>
    </div>
    
    <hr />

    <div v-for="x in 33-inputPrefix">
        <details>
            <summary>
                네트워크 수: {{ 2**(x-1) }} (분할 {{ x-1 }} 회) , 규모: {{ 2**(32-(inputPrefix+x-1)) }} , <span style="color:red">가용규모: {{ Math.max(0, 2**(32-(inputPrefix+x-1)) - 2) }}</span> , Prefix (Subnet Mask): /{{ inputPrefix+x-1 }} ({{ prefix_to_subnetmask(inputPrefix+x-1) }})
            </summary>
            <table>
                <tbody>
                    <tr>
                        <th scope="col">네트워크 주소</th>
                        <th scope="col">가용 주소</th>
                        <th scope="col">브로드캐스트 주소</th>
                    </tr>
                    <tr v-for="y in 2**(x-1)">
                        <td>{{ getNetAddr(inputNetAddr, inputPrefix+x-1, y-1) }}</td>
                        <td>{{ getUsableAddrStart(inputNetAddr, inputPrefix+x-1, y-1) }} ~ {{ getUsableAddrEnd(inputNetAddr, inputPrefix+x-1, y-1) }}</td>
                        <td>{{ getBroadCastAddr(inputNetAddr, inputPrefix+x-1, y-1) }} </td>
                    </tr>
                </tbody>
            </table>
        </details>
    </div>


</template>


<script>

export default {
    name: "App",
    data() {
        return {
            inputNetAddr: "192.168.10.0",
            inputPrefix: 24
        }
    },
    methods: {
        handleValidate() {
            alert("TODO")
        },
        prefix_to_subnetmask(prefix) {
            let subnetmask = []
            let binary = "1".repeat(prefix) + "0".repeat(32-prefix)
            for (let i = 0; i < 4; i++) {
                subnetmask.push(parseInt(binary.slice(8*i, 8*i+8), 2))
            }
            return subnetmask.join(".")
        },
        decimal_addr_to_binary_addr(decimal_addr) {
            let binary_addr = ""
            for (let i of decimal_addr.split(".")) {
                binary_addr += parseInt(i, 10).toString(2).padStart(8, "0")
            }
            return binary_addr
        },
        binary_addr_to_decimal_addr(binary_addr) {
            let decimal_addr = []
            for (let i = 0; i < 4; i++) {
                decimal_addr.push(parseInt(binary_addr.slice(8*i, 8*i+8), 2))
            }
            return decimal_addr.join(".")
        },
        getNetAddr(inputNetAddr, prefix, y) {
            let netAddr = ""
            let binaryNetAddr = this.decimal_addr_to_binary_addr(inputNetAddr)
            netAddr += binaryNetAddr.slice(0, this.inputPrefix)
            if (prefix-this.inputPrefix >= 1) {
                netAddr += y.toString(2).padStart(prefix-this.inputPrefix, "0")
            }
            netAddr += "0".repeat(32-prefix)
            return this.binary_addr_to_decimal_addr(netAddr)
        },
        getUsableAddrStart(inputNetAddr, prefix, y){
            let netAddr = ""
            let binaryNetAddr = this.decimal_addr_to_binary_addr(inputNetAddr)
            netAddr += binaryNetAddr.slice(0, this.inputPrefix)
            if (prefix-this.inputPrefix >= 1) {
                netAddr += y.toString(2).padStart(prefix-this.inputPrefix, "0")
            }
            netAddr += "0".repeat(32-prefix)
            if (prefix <= 30) {
                return this.binary_addr_to_decimal_addr((parseInt(netAddr, 2) + parseInt("1", 2)).toString(2).padStart(32, "0"))
            } else {
                return "None"
            }
        },
        getUsableAddrEnd(inputNetAddr, prefix, y){
            let broadCastAddr = ""
            let binaryNetAddr = this.decimal_addr_to_binary_addr(inputNetAddr)
            broadCastAddr += binaryNetAddr.slice(0, this.inputPrefix)
            if (prefix-this.inputPrefix >= 1) {
                broadCastAddr += y.toString(2).padStart(prefix-this.inputPrefix, "0")
            }
            broadCastAddr += "1".repeat(32-prefix)
            
            if (prefix <= 30) {
                return this.binary_addr_to_decimal_addr((parseInt(broadCastAddr, 2) - parseInt("1", 2)).toString(2).padStart(32, "0"))
            } else {
                return "None"
            }
        },
        getBroadCastAddr(inputNetAddr, prefix, y) {
            let broadCastAddr = ""
            let binaryNetAddr = this.decimal_addr_to_binary_addr(inputNetAddr)
            broadCastAddr += binaryNetAddr.slice(0, this.inputPrefix)
            if (prefix-this.inputPrefix >= 1) {
                broadCastAddr += y.toString(2).padStart(prefix-this.inputPrefix, "0")
            }
            broadCastAddr += "1".repeat(32-prefix)
            
            if (prefix <= 31) {
                return this.binary_addr_to_decimal_addr(broadCastAddr)
            } else {
                return "None"
            }
        }
    }
}
</script>


<style> 
</style> 
