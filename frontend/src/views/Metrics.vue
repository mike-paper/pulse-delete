<template>
  <div class="bg-gray-900">
    <div v-if="!storeState.gotMetrics">
      <div class="flex justify-center space-y-8 w-full pt-32">
        <svg class="animate-spin -ml-1 mr-3 h-20 w-20 text-gray-100" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>
    </div>
    <div v-else class="">
      <div class="">
        <!-- <div id="view">
          vega
        </div> -->
        <!-- This example requires Tailwind CSS v2.0+ -->
        <dl class="mt-5 grid grid-cols-1 bg-gray-900 overflow-hidden divide-y divide-gray-800 md:grid-cols-3 md:divide-y-0 md:divide-x">
          <div class="px-4 py-5 sm:p-6 hover:bg-gray-800">
            <dt class="text-base font-normal text-gray-500">
              MRR
            </dt>
            <dd class="mt-1 flex justify-between items-baseline md:block lg:flex">
              <div @click="drillDown('mrr')" class="flex items-baseline text-4xl font-semibold text-gray-100 cursor-pointer">
                ${{(storeState.metricData.summary[2].mrr/1000).toFixed(1)}}k
                <span class="ml-2 text-sm font-medium text-gray-500"> 
                  from ${{(storeState.metricData.summary[1].mrr/1000).toFixed(1)}}k
                </span>
              </div>

              <div :class="['increase' === 'increase' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800', 'inline-flex items-baseline px-2 py-1 rounded-full text-sm font-medium md:mt-2 lg:mt-0']">
                <ArrowSmUpIcon v-if="'increase' === 'increase'" class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5 text-green-500" aria-hidden="true" />
                <ArrowSmDownIcon v-else class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5 text-red-500" aria-hidden="true" />
                <span class="sr-only"> {{ 'increase' === 'increase' ? 'Increased' : 'Decreased' }} by </span>
                ${{((storeState.metricData.summary[2].mrr-storeState.metricData.summary[1].mrr)/1000).toFixed(1)}}k
              </div>
            </dd>
          </div>
          <div class="px-4 py-5 sm:p-6 hover:bg-gray-800">
            <dt class="text-base font-normal text-gray-500">
              Customers
            </dt>
            <dd class="mt-1 flex justify-between items-baseline md:block lg:flex">
              <div class="flex items-baseline text-4xl font-semibold text-gray-100">
                {{Math.round(storeState.metricData.summary[2].active)}}
                <span class="ml-2 text-sm font-medium text-gray-500"> 
                  from {{Math.round(storeState.metricData.summary[1].active)}}
                </span>
              </div>

              <div :class="['increase' === 'increase' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800', 'inline-flex items-baseline px-2 py-1 rounded-full text-sm font-medium md:mt-2 lg:mt-0']">
                <ArrowSmUpIcon v-if="'increase' === 'increase'" class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5 text-green-500" aria-hidden="true" />
                <ArrowSmDownIcon v-else class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5 text-red-500" aria-hidden="true" />
                <span class="sr-only"> {{ 'increase' === 'increase' ? 'Increased' : 'Decreased' }} by </span>
                {{(Math.round(storeState.metricData.summary[2].active-storeState.metricData.summary[1].active))}}
              </div>
            </dd>
          </div>
          <div class="px-4 py-5 sm:p-6 hover:bg-gray-800">
            <dt class="text-base font-normal text-gray-500">
              Churn
            </dt>
            <dd class="mt-1 flex justify-between items-baseline md:block lg:flex">
              <div class="flex items-baseline text-4xl font-semibold text-gray-100">
                ${{(storeState.metricData.summary[2].churned_mrr/1000).toFixed(1)}}k
                <span class="ml-2 text-sm font-medium text-gray-500"> 
                  from ${{(storeState.metricData.summary[1].churned_mrr/1000).toFixed(1)}}k
                </span>
              </div>

              <div :class="['increase' === 'increase' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800', 'inline-flex items-baseline px-2 py-1 rounded-full text-sm font-medium md:mt-2 lg:mt-0']">
                <ArrowSmUpIcon v-if="'increase' === 'increase'" class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5 text-green-500" aria-hidden="true" />
                <ArrowSmDownIcon v-else class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5 text-red-500" aria-hidden="true" />
                <span class="sr-only"> {{ 'increase' === 'increase' ? 'Increased' : 'Decreased' }} by </span>
                ${{((storeState.metricData.summary[2].churned_mrr-storeState.metricData.summary[1].churned_mrr)/1000).toFixed(1)}}k
              </div>
            </dd>
          </div>
        </dl>
        <div 
          class="grid bg-gray-900 overflow-hidden divide-y divide-gray-800 md:grid-cols-3 md:divide-y-0 md:divide-x"
        >
          <div 
            id="mrr" 
            class="hover:bg-gray-800"
          >
            mrr
          </div>
          <div id="customers" class="hover:bg-gray-800">
            customers
          </div>
          <div id="churn" class="hover:bg-gray-800">
            churn
          </div>
          <div id="ltv" class="hover:bg-gray-800">
            <div class="px-4 py-5 sm:p-6 hover:bg-gray-800">
              <div class="text-base font-normal text-gray-500">
                LTV (Life Time Value)
              </div>
              <div class="text-gray-500 grid grid-cols-3 border-b border-dashed border-gray-500 mt-4">
                <div class="col-span-1">
                  <div class="inline">
                    ARPU 
                  </div>
                   <Popper class="inline" hover>
                    <QuestionMarkCircleIcon class="mb-1 inline h-5 w-5 text-gray-500" aria-hidden="true" />
                    <template #content>
                      <div class="bg-gray-700 text-gray-100 px-3 py-2 rounded">Average revenue per user</div>
                    </template>
                  </Popper>
                </div>
                <div class="col-span-1">
                  
                </div>
                <div class="col-span-1 text-right">
                  <!-- ${{(storeState.metricData.ltv.arpu).toFixed(0)}}  -->
                  {{ssfFormatter('$#,##0', storeState.metricData.ltv.arpu)}}
                </div>
              </div>
              <div class="text-gray-500 grid grid-cols-3 border-b border-dashed border-gray-500 mt-4">
                <div class="col-span-1">
                  <div class="inline">
                    Churn
                  </div>
                   <Popper class="inline" hover>
                    <QuestionMarkCircleIcon class="mb-1 inline h-5 w-5 text-gray-500" aria-hidden="true" />
                    <template #content>
                      <div class="bg-gray-700 text-gray-100 px-3 py-2 rounded">Revenue % churn last 3 month average</div>
                    </template>
                  </Popper>
                </div>
                <div class="col-span-1">
                  
                </div>
                <div class="col-span-1 text-right">
                  {{(storeState.metricData.ltv.churn_rate*100).toFixed(1)}}%
                </div>
              </div>
              <div class="text-gray-500 grid grid-cols-3 border-b border-dashed border-gray-500 mt-4">
                <div class="col-span-1">
                  <div class="inline">
                    Lifetime
                  </div>
                   <Popper class="inline" hover>
                    <QuestionMarkCircleIcon class="mb-1 inline h-5 w-5 text-gray-500" aria-hidden="true" />
                    <template #content>
                      <div class="bg-gray-700 text-gray-100 px-3 py-2 rounded">Average # of months a customer pays you</div>
                    </template>
                  </Popper>
                </div>
                <div class="col-span-1">
                  
                </div>
                <div class="col-span-1 text-right">
                  {{(storeState.metricData.ltv.lifetime_months).toFixed(1)}} months 
                </div>
              </div>
              <div class="text-gray-500 grid grid-cols-3 border-b border-dashed border-gray-500 mt-4">
                <div class="col-span-1">
                  <div class="inline">
                    CLV
                  </div>
                   <Popper class="inline" hover>
                    <QuestionMarkCircleIcon class="mb-1 inline h-5 w-5 text-gray-500" aria-hidden="true" />
                    <template #content>
                      <div class="bg-gray-700 text-gray-100 px-3 py-2 rounded">Customer lifetime value</div>
                    </template>
                  </Popper>
                </div>
                <div class="col-span-1">
                  
                </div>
                <div class="col-span-1 text-right">
                  {{ssfFormatter('$#,##0', storeState.metricData.ltv.clv)}}
                </div>
              </div>
            </div>
          </div>
          <div class="col-span-2">
            <div id="retention" class="hover:bg-gray-800">
              retention
            </div>
          </div>
        </div>
        <div>
        </div>
        
      </div>
      <!-- <div class="-mb-16 float-right mt-4 right-0 z-10" id="somethingelse">
        <SwitchGroup as="div" class="flex items-center">
          <Switch v-model="tableFilters.active" :class="[tableFilters.active ? 'bg-indigo-600' : 'bg-gray-200', 'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500']">
            <span class="sr-only">Use setting</span>
            <span aria-hidden="true" :class="[tableFilters.active ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none inline-block h-5 w-5 rounded-full bg-gray-900 shadow transform ring-0 transition ease-in-out duration-200']" />
          </Switch>
          <SwitchLabel as="span" class="ml-3 mr-4">
            <span class="text-sm font-medium text-gray-100">Active only</span>
          </SwitchLabel>
        </SwitchGroup>
      </div> -->
      <div id="customerTable">
        
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable no-unused-vars */
import { store } from '../store.js';
import { reactive, ref } from 'vue'
import { Switch, SwitchGroup, SwitchLabel } from '@headlessui/vue'
import axios from 'axios';
import * as vega from "vega";
import SSF from 'ssf'
// import embed from 'vega-embed';
// import * as embed from "vega-embed";
// embed = require('vega-embed')

import { Grid, html } from "gridjs";
// import "gridjs/dist/theme/mermaid.css";

import { ArrowSmUpIcon, ArrowSmDownIcon, QuestionMarkCircleIcon } from '@heroicons/vue/solid'

import Popper from "vue3-popper";

export default {
  name: 'Metrics',
  props: {
      msg: String
  },
  components: {
    ArrowSmUpIcon,
    ArrowSmDownIcon,
    QuestionMarkCircleIcon,
    Popper
    // Switch,
    // SwitchGroup,
    // SwitchLabel,
  },
  created() {
    var yourVlSpec = {
      $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
      description: 'A simple bar chart with embedded data.',
      data: {
        values: [
          {a: 'A', b: 28},
          {a: 'B', b: 55},
          {a: 'C', b: 43},
          {a: 'D', b: 91},
          {a: 'E', b: 81},
          {a: 'F', b: 53},
          {a: 'G', b: 19},
          {a: 'H', b: 87},
          {a: 'I', b: 52}
        ]
      },
      mark: 'bar',
      encoding: {
        x: {field: 'a', type: 'ordinal'},
        y: {field: 'b', type: 'quantitative'}
      }
    };
    window.customerGrid = new Grid({
      sort: true,
      search: true,
      pagination: {
        limit: 20
      },
      fixedHeader: true,
      height: '400px',
      // columns: ["Name", "Email", "Phone Number"],
      columns: [{
        id: 'mrr_month_dt',
        name: 'Date (as of)',
        formatter: (cell) => `${new Date(cell).toLocaleDateString("en-US")}`
      }, {
        id: 'email',
        name: 'Email'
      }, {
        id: 'customer_id',
        name: 'Customer ID',
        formatter: (cell) => html(
          `<a class="font-medium text-blue-500 hover:text-blue-900 transition duration-150 ease-in-out" href="https://dashboard.stripe.com/customers/${cell}" target="_blank">
            ${cell}
          </a>
          `
          )
      }, {
        id: 'mrr_status',
        name: 'Status'
      }, {
        id: 'mrr',
        name: 'MRR'
      }, {
        id: 'canceled_dt',
        name: 'Canceled On',
        formatter: (cell) => `${cell ? new Date(cell).toLocaleDateString("en-US") : ''}`
      }, 
      ],
      data: [],
      className: {
        td: 'px-6 py-4 whitespace-nowrap text-sm text-gray-100 divide-y divide-gray-200',
        th: 'px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 tracking-wider',
        table: 'min-w-full divide-gray-200',
        tbody: 'bg-gray-900 '
      }
    })
    // window.vegaEmbed('#view', yourVlSpec);
  },
  mounted() {
    this.emitter.on('user-login', d => {
      // this.getMetrics()
    });
    this.emitter.on('got-metrics', d => {
      this.createCharts()
      var self = this
      // setTimeout(() => self.createCustomerTable(), 0);
    });
    if (this.storeState.gotMetrics) {
      this.createCharts()
      var self = this
      // setTimeout(() => self.createCustomerTable(), 0);
    }
    // this.startTyped()
  },
  data() {
      return {
        store: store,
        storeState: store.state,
        gotMetrics: false,
        tableFilters: {
          active: false,
        },
        // metricData: [],
        stats: [
          { name: 'Total Subscribers', stat: '71,897', previousStat: '70,946', change: '12%', changeType: 'increase' },
          { name: 'Avg. Open Rate', stat: '58.16%', previousStat: '56.14%', change: '2.02%', changeType: 'increase' },
          { name: 'Avg. Click Rate', stat: '24.57%', previousStat: '28.62%', change: '4.05%', changeType: 'decrease' },
        ],
        vegaConfig: {
          "view": {
            "stroke": "transparent"
          },
          "arc": {"fill": "#fff"},
          "area": {"fill": "#fff"},
          "path": {"stroke": "#fff"},
          "rect": {"fill": "#fff"},
          "shape": {"stroke": "#fff"},
          "symbol": {"stroke": "#fff"},
          "circle": {"fill": "#fff"},
          "background": "transparent",
          "padding": {"top": 10, "right": 10, "bottom": 10, "left": 10},
          "style": {
            "guide-label": {"font": "Inter, sans-serif", "fontSize": 12},
            "guide-title": {"font": "Inter, sans-serif", "fontSize": 12},
            "group-title": {"font": "Inter, sans-serif", "fontSize": 12}
          },
          "axis": {
            "gridColor": "#f7fafc",
            "tickColor": "transparent",
            "labelColor": "#f7fafc",
            "domain": false,
          }
        },
        vegaSpec: {
          "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
          "description": "MRR by Month",
          "width": "container",
          "mark": {
            "type": "line", 
            "tooltip": false, 
            "fill": null, 
            "stroke": "#9ae6b4",
            "point": {"color": "#9ae6b4"},
            },
          "encoding": {
              "x": {},
              "y": {},
          },
          data: {values: []},
        },
      }
  },
  methods: {
    login() {
      this.$router.push({ name: 'Login', query: { goto: 'Landing' }})
    },
    logout() {
      this.$router.push({ name: 'Logout', query: { goto: 'Landing' }})
    },
    drillDown(drillOn) {
      this.$router.push({ name: 'Analyze', query: { drill: drillOn}})
    },
    goToAnalyze() {
      this.$router.push({ name: 'Analyze', query: { uuid: 'mrrchart' }})
    },
    generateDemoTable() {
      new Grid({
        sort: true,
        search: true,
        columns: ["Name", "Email", "Phone Number"],
        data: [
          ["John", "john@example.com", "(353) 01 222 3333"],
          ["Mark", "mark@gmail.com", "(01) 22 888 4444"],
          ["Eoin", "eoin@gmail.com", "0097 22 654 00033"],
          ["Sarah", "sarahcdd@gmail.com", "+322 876 1233"],
          ["Afshin", "afshin@mail.com", "(353) 22 87 8356"]
        ],
        className: {
          td: 'px-6 py-4 whitespace-nowrap text-sm text-gray-100 divide-y divide-gray-200',
          th: 'px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider',
          table: 'min-w-full divide-gray-200',
          tbody: 'bg-gray-900 '
        }
      }).render(document.getElementById("testtable"));
    },
    createCustomerTable() {
      // window.customerGrid.render(document.getElementById("customerTable"));
      let data = this.storeState.metricData.data.filter(o => (this.tableFilters.active ? o.status === 'active' : true) && o.current_month === 1)
      data
      console.log('createCustomerTable...', data.length)
      window.customerGrid.updateConfig({
      // lets update the columns field only
        data: data
      })
      if (window.customerGrid.config.container) {
        window.customerGrid.forceRender()
      } else {
        window.customerGrid.render(document.getElementById("customerTable"));
      }
      // document.getElementById("customerTable").innerHTML = ''
    },
    getApiUrl(endpoint) {
      if (process.env.NODE_ENV != 'production') return `http://127.0.0.1:5000/${endpoint}`
      return `https://pulse-backend.onrender.com/${endpoint}`
    },
    getAppUrl(endpoint) {
      if (process.env.NODE_ENV != 'production') return `http://localhost:8080/${endpoint}`
      return `https://trypaper.io/${endpoint}`
    },
    updateSavedFunders() {
      this.storeState.userData.savedFunders = []
      for (let index = 0; index < this.filteredFunders.length; index++) {
        const row = this.filteredFunders[index];
        if (row.saved) this.storeState.userData.savedFunders.push(row.public_id)
      }
      this.updateUserData()
    },
    updateSavedOnFunders() {
      for (let index = 0; index < this.funderData.length; index++) {
        const f = this.funderData[index]
        if (this.storeState.userData.savedFunders.includes(f.public_id)) f.saved = true
      }
    },
    saveFunder(row) {
      row.saved = true
      if (!this.storeState.isLoggedIn || !this.storeState.user.publicAddress) {
        this.$router.push({ name: 'Login', query: { goto: 'Landing' }})
      }
    },
    updateUserData() {
      if (!this.storeState.isLoggedIn || !this.storeState.gotUserData) return
      const path = this.getApiUrl('update_user_data')
      let d = {user: this.storeState.user, userData: this.storeState.userData}
      axios.post(path, d)
        .then((res) => {
          console.log('got update_user_data: ', res.data)
        })
        .catch((error) => {
          console.error(error)
        })
    },
    removeFunder(row) {
      row.saved = false
      // this.storeState.userData.savedFunders.pop(row.domain)
      if (!this.storeState.isLoggedIn || !this.storeState.user.publicAddress) {
        this.$router.push({ name: 'Login', query: { goto: 'Landing' }})
      } else {
        // save funder to users db
        this.updateUserData()
      }
    },
    applyNow() {
      this.$router.push({ name: 'Apply'})
    },
    applyToFunder(row) {
      this.saveFunder(row)
      if (!this.storeState.isLoggedIn || !this.storeState.user.publicAddress) {
        this.$router.push({ name: 'Login', query: { goto: 'Landing' }})
      } else {
        let url = `http://${row.domain}/?ref=trypaperio`
        window.open(url, '_blank');
      }
    },
    moreInfo(row) {
      // this.saveFunder(row)
      if (!this.storeState.isLoggedIn || !this.storeState.user.publicAddress) {
        this.$router.push({ name: 'Login', query: { goto: 'Landing' }})
      } else {
        let url = `http://${row.domain}/?ref=trypaperio`
        window.open(url, '_blank');
      }
    },
    filterFunders() {
      this.filteredFunders = this.funderData
      if (!this.storeState.isLoggedIn) {
        this.filteredFunders = this.funderData.slice(0, 10)
      }
      if (this.revenue.value > 0) {
        this.filteredFunders = this.filteredFunders.filter(row => row.min_annual_revenue <= this.revenue.value)
      }
      if (this.product.value != 'all') {
        this.filteredFunders = this.filteredFunders.filter(row => row.loan_type === this.product.value)
      }
      if (this.rating.value != 'all') {
        let ls = []
        for (let index = 0; index < this.filteredFunders.length; index++) {
          const row = this.filteredFunders[index]
          let rating = this.formatRank(row.paper_rank)
          if (rating <= this.rating.value) ls.push(row)
        }
        this.filteredFunders = ls
      }
      if (this.searchTerm.length > 0) {
        this.filteredFunders = this.filteredFunders.filter(row => row.name.toLowerCase().includes(this.searchTerm.toLowerCase()))
      }
      
    },
    createCharts() {
      let opts = {
        config: this.vegaConfig,
        actions: false,
        tooltip: {theme: 'custom'},
        }
      this.createRetentionChart()
      // let mrr = this.deepCopy(this.vegaSpec)
      // mrr.data.values = this.storeState.metricData.data
      // window.vegaEmbed('#mrr', mrr, opts);
      let mrr = this.deepCopy(this.vegaSpec)
      mrr.data.values = this.storeState.metricData.data
      mrr.layer = [
        {
          "encoding": {
            "color": {"value": "#9ae6b4"},
            "y": {"field": "mrr", "type": "quantitative"}
          },
          "layer": [
            {
              "mark": "line", 
              "color": "#9ae6b4",
              "point": {"color": "#9ae6b4"},
            },
          ]
        },
        {
          "mark": "rule",
          "encoding": {
            "opacity": {
              "value": 0,
            },
            "tooltip": [
                {"field": "mrr_month_dt", "timeUnit": "yearmonth", "title": "Date"},
                {
                  "field": "mrr", 
                  "aggregate": "sum", 
                  "type": "quantitative",
                  "format": "$,.0f",
                  "title": "MRR"
                }
            ]
          },
          "params": [{
            "name": "hover",
            "select": {
              "type": "point",
              "fields": ["mrr_month_dt"],
              "nearest": true,
              "on": "mouseover",
              "clear": "mouseout"
            }
          }]
        }
      ]
      mrr.encoding = {
          "x": {
            "field": "mrr_month_dt", 
            "timeUnit": "yearmonth", 
            "title": null,
            "axis": {
              "values": [
                {"year": 2019, "month": "may", "date": 1},
                {"year": 2021, "month": "may", "date": 1}
                ],
              "grid": false,
              },
              "labelColor": "#fff",
              
            },
          "y": {
            "field": "mrr", 
            "aggregate": "sum", 
            "type": "quantitative",
            "title": null,
            "grid": false,
            "axis": {
              "grid": true,
              "gridOpacity": 0.2,
              "gridDash": {
                "value": [2, 2]
              },
            }
          },
      }
      window.vegaEmbed('#mrr', mrr, opts);
      let customers = this.deepCopy(this.vegaSpec)
      customers.data.values = this.storeState.metricData.data
      customers.layer = [
        {
          "encoding": {
            "color": {"value": "#9ae6b4"},
            "y": {"field": "active", "type": "quantitative"}
          },
          "layer": [
            {
              "mark": "line", 
              "color": "#9ae6b4",
              "point": {"color": "#9ae6b4"},
            },
          ]
        },
        {
          "mark": "rule",
          "encoding": {
            "opacity": {
              "value": 0,
            },
            "tooltip": [
                {"field": "mrr_month_dt", "timeUnit": "yearmonth", "title": "Date"},
                {
                  "field": "active", 
                  "aggregate": "sum", 
                  "type": "quantitative",
                  "format": ",.0f",
                  "title": "Customers"
                }
            ]
          },
          "params": [{
            "name": "hover",
            "select": {
              "type": "point",
              "fields": ["mrr_month_dt"],
              "nearest": true,
              "on": "mouseover",
              "clear": "mouseout"
            }
          }]
        }
      ]
      customers.encoding = {
          "x": {
            "field": "mrr_month_dt", 
            "timeUnit": "yearmonth", 
            "title": null,
            "axis": {
              "values": [
                {"year": 2019, "month": "may", "date": 1},
                {"year": 2021, "month": "may", "date": 1}
                ],
              "grid": false,
              },
              "labelColor": "#fff",
              
            },
          "y": {
            "field": "active", 
            "aggregate": "sum", 
            "type": "quantitative",
            "title": null,
            "grid": false,
            "axis": {
              "grid": true,
              "gridOpacity": 0.2,
              "gridDash": {
                "value": [2, 2]
              },
            }
          },
      }
      window.vegaEmbed('#customers', customers, opts);
      let churn = this.deepCopy(this.vegaSpec)
      churn.data.values = this.storeState.metricData.data
      churn.layer = [
        {
          "encoding": {
            "color": {"value": "#9ae6b4"},
            "y": {"field": "churned_mrr", "type": "quantitative"}
          },
          "layer": [
            {
              "mark": "line", 
              "color": "#9ae6b4",
              "point": {"color": "#9ae6b4"},
            },
          ]
        },
        {
          "mark": "rule",
          "encoding": {
            "opacity": {
              "value": 0,
            },
            "tooltip": [
                {"field": "mrr_month_dt", "timeUnit": "yearmonth", "title": "Date"},
                {
                  "field": "churned_mrr", 
                  "aggregate": "sum", 
                  "type": "quantitative",
                  "format": "$,.0f",
                  "title": "Customers"
                }
            ]
          },
          "params": [{
            "name": "hover",
            "select": {
              "type": "point",
              "fields": ["mrr_month_dt"],
              "nearest": true,
              "on": "mouseover",
              "clear": "mouseout"
            }
          }]
        }
      ]
      churn.encoding = {
          "x": {
            "field": "mrr_month_dt", 
            "timeUnit": "yearmonth", 
            "title": null,
            "axis": {
              "values": [
                {"year": 2019, "month": "may", "date": 1},
                {"year": 2021, "month": "may", "date": 1}
                ],
              "grid": false,
              },
              "labelColor": "#fff",
              
            },
          "y": {
            "field": "churned_mrr", 
            "aggregate": "sum", 
            "type": "quantitative",
            "title": null,
            "grid": false,
            "axis": {
              "grid": true,
              "gridOpacity": 0.2,
              "gridDash": {
                "value": [2, 2]
              },
            }
          },
      }
      window.vegaEmbed('#churn', churn, opts);
    },
    createRetentionChart() {
      let opts = {
        config: this.vegaConfig,
        actions: false,
        tooltip: {theme: 'custom'},
      }
      let vegaSpec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        data: {values: this.storeState.metricData.retention},
        "transform": [
          {
            // "aggregate": [{"revenue_retention": "count", "as": "revenue_retention"}],
            "groupby": ["vintage", "vintage_age"]
          }
        ],
        "encoding": {
          "y": {"field": "vintage", "type": "ordinal"},
          "x": {"field": "vintage_age", "type": "ordinal"}
        },
        "layer": [
          {
            "mark": "rect",
            "encoding": {
              "color": {
                "field": "revenue_retention",
                "type": "quantitative",
                "title": "Revenue Retention",
                "legend": {"direction": "horizontal", "gradientLength": 120}
              }
            }
          },
          {
            "mark": "text",
            "encoding": {
              "text": {"field": "revenue_retention", "type": "quantitative"},
              "color": {
                "condition": {"test": "datum['revenue_retention'] < .5", "value": "black"},
                "value": "white"
              }
            }
          }
        ],
        "config": {
          "axis": {"grid": true, "tickBand": "extent"}
        }
      }
      window.vegaEmbed('#retention', vegaSpec, opts);
    },
    deepCopy(c) {
      return JSON.parse(JSON.stringify(c))
    },
    getFunded() {
      this.$router.push({ name: 'Apply', params: { userId: 123 }})
    },
    goToFunders() {
      this.$router.push({ name: 'Login', params: { userId: 123 }})
    },
    getRequiredMrr() {
      return ((this.loan.amount / this.loan.multiple) / 1000).toFixed(0)
    },
    setPayoutPeriod(po) {
      this.loan.payoutPeriod = po
      this.updatingPayoutPeriod = false
    },
    calcLoan() {
      let month = 0
      this.loan.months = []
      this.loan.years = []
      this.loan.totalPayback = 0
      this.loan.totalInterest = 0
      while (this.loan.term > month) {
        var payback = 0
        var payout = 0
        var balance = 0
        // payout = this.loan.amount / this.loan.payoutPeriod.months
        if (month <= this.loan.payoutPeriod.months - 1) {
          payout = this.loan.amount / this.loan.payoutPeriod.months
        }
        if (month == 0) {
          balance = payout
        } else {
          let prevMonth = this.loan.months[month-1]
          balance = payout + prevMonth.interest + prevMonth.balance
        }
        let interest = balance * (this.loan.rate / 12)
        
        if (month > 23) { //start paying back
          let mo23Bal = this.loan.months[22].balance
          let prevMonth = this.loan.months[month-1]
          payback = (mo23Bal / 12) + prevMonth.interest + prevMonth.payout
        } else if (month > 11) { //start paying interest
          payback = this.loan.months[month-1].interest
        }
        balance = balance - payback
        this.loan.totalPayback+=payback
        this.loan.totalInterest+=interest
        let m = {
          month: month,
          payback: payback,
          payout: payout,
          balance: balance,
          interest: interest
        }
        this.loan.months.push(m)
        if (Object.keys(this.yearLookup).includes(String(month))) {
          m.label = this.yearLookup[month]
          this.loan.years.push(m)
        }
        month+=1
      }
    },
    ssfFormatter(format, val) {
      // return (m / 1000).toFixed(1)
      return SSF.format(format, val)
    },
  },
  watch: {
    'tableFilters': {
        handler: function () {
          this.createCustomerTable()
        },
        deep: true
    },
  },
}
/* eslint-disable no-unused-vars */
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
  #vg-tooltip-element.vg-tooltip.custom-theme {
    color: #f7fafc;
  }
  #vg-tooltip-element table tr td.key {
    color: #718096;
  }
  #vg-tooltip-element {
    background-color: #2d3748;
    color: #f7fafc;
    border: none;
  }
</style>
