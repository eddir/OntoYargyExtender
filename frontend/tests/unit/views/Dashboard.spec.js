import Vue from 'vue'
import regeneratorRuntime from "regenerator-runtime";
import { shallowMount } from '@vue/test-utils'
import CoreuiVue from '@coreui/vue'
import Filler from '@/views/filler/Filler.vue'


Vue.use(regeneratorRuntime)
Vue.use(CoreuiVue)

describe('Filler.vue', () => {
  it('has a name', () => {
    expect(Filler.name).toBe('Filler')
  })
  it('is Vue instance', () => {
    const wrapper = shallowMount(Filler)
    expect(wrapper.vm).toBeTruthy()
  })
  it('is Dashboard', () => {
    const wrapper = shallowMount(Filler)
    expect(wrapper.findComponent(Filler)).toBeTruthy()
  })
  test('renders correctly', () => {
    const wrapper = shallowMount(Filler)
    expect(wrapper.element).toMatchSnapshot()
  })
})
