<template>
  <div>
    <v-braintree
      v-if="clientToken"
      :authorization="clientToken"
      @success="onSuccess"
      @error="onError"
    ></v-braintree>
  </div>
</template>

<script>
import { getClientId } from "@/api";
export default {
  props: ['custCode'],
  mounted(){
    this.setClientToken();
  },
  data() {
    return {
      clientToken: false,
      nonce: false,
      payment_token: "",
      cardParams: {
        cardholderName: {
          required: true,
        },
      },
    };
  },
  methods: {
    onSuccess(payload) {
      this.nonce = payload.nonce;
      console.log('success');
    },
    onError(error) {
      let message = error.message;
      console.error(message);
    },
    onLoadFail(error) {
      alert("load failed");
      console.error(error);
    },
    setClientToken() {
      getClientId(this.custCode)
        .then((resp) => {
          console.log("getClientID Resp ", resp);
          this.clientToken = resp.data.clientToken;
          this.client_id = resp.data.customer_id;
        })
        .catch((error) => console.error(error));
    },
  },
};
</script>
