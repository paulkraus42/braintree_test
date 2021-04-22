<!--suppress CssUnknownTarget -->
<template>
    <div>
        <div id="main-container">
            payment
            <Payment custCode="0000000500"></Payment>
        </div>
    </div>
</template>

<script>
    import Payment from "./Payment"

    export default {
        components: {Payment},
    }
</script>
