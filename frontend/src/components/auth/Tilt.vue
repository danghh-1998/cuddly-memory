<template>
    <div
        class="tilt"
        :class="cls"
        @mouseenter="enter"
        @mousemove="move"
        @mouseleave="leave"
    >
        <slot />
    </div>
</template>

<script>
    export default {
        name: "Tilt",
        props: {
            max: {
                type: Number,
                default: 40
            },
            // eslint-disable-next-line vue/require-default-prop
            cls: {
                type: String,
                required: false
            },
            perspective: {
                type: Number,
                default: 500
            },
            reverse: {
                type: Boolean,
                default: false
            }
        },
        data: function () {
            return {
                timer: null
            }
        },
        computed: {
            reverseValue() {
                return this.reverse ? -1 : 1;
            }
        },
        mounted: function () {
            this.$el.style.cssText = `
                transform-origin: center;
                will-change: transform;
                `;
        },
        methods: {
            getPosition(el) {
                const box = el.getBoundingClientRect();
                return {
                    left: box.left,
                    top: box.top,
                    width: box.width,
                    height: box.height
                };
            },
            toggleTransition() {
                if (this.timer) clearTimeout(this.timer);

                this.$el.style.transition = `all 150ms linear`;
                this.timer = setTimeout(() => {
                    this.$el.style.transition = '';
                }, 150);
            },
            enter() {
                this.toggleTransition();
            },
            move(e) {
                const pos = this.getPosition(this.$el);

                let x = Math.min((e.clientX - pos.left) / this.$el.offsetWidth, 1);
                let y = Math.min((e.clientY - pos.top) / this.$el.offsetHeight, 1);

                let X = this.reverseValue * (this.max / 2 - x * this.max);
                let Y = this.reverseValue * (y * this.max - this.max / 2);

                this.$el.style.transform = `perspective(${this.perspective}px) rotateX(${Y}deg) rotateY(${X}deg)`;
            },
            leave() {
                this.toggleTransition();

                this.$el.style.transform = `perspective(${this.perspective}px) rotateX(0) rotateY(0)`
            }
        }
    }
</script>

<style scoped>

</style>