import Vue from 'vue'

let axiosConfig = {
    headers: {Authorization: 'Bearer ' + localStorage.getItem('token')}
}

export function getClientId(customerId){
    let requestDict = {...axiosConfig};
    requestDict.params = {
        customerId: customerId
    };
    return Vue.axios.get('/bt/get_client_token', requestDict);
}

export function vaultCustomer(payload){
    let requestDict = {...axiosConfig};
    console.log('vaultCustomer', payload)
    requestDict.params = {
        payload: payload
    };
    console.log('requsetDict', requestDict)
    return Vue.axios.post('/bt/vault_customer', {payload:payload});
}
