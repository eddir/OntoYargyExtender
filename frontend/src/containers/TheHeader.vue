<template>
  <CHeader fixed with-subheader light class="d-block d-md-none">
    <CHeaderNav class="mr-auto overflow-auto">
      <CHeaderNavItem v-for="item in items" :key="item._name" class="px-3">
        <CHeaderNavLink :to="item.to">
          {{ item.name }}
        </CHeaderNavLink>
      </CHeaderNavItem>
    </CHeaderNav>
    <CSubheader class="px-3">
      <CBreadcrumbRouter class="border-0 mb-0"/>
    </CSubheader>
  </CHeader>
</template>

<script>
import nav from './_nav'
export default {
  name: 'TheHeader',
  data () {
    return {
      items: nav[0]._children
    }
  }
}
</script>
