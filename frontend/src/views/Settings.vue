<template>
  <div>
    <div v-if="!true">
      Spinning...
    </div>
    <div v-else>
      <div class="pt-8 pl-8">
        <div class="text-3xl font-extrabold text-gray-900">
          Settings
        </div>
        <div class="pt-8">
          <div class="font-medium leading-6 text-gray-900 text-lg">
            Notifications
          </div>
          <p class="max-w-2xl text-sm text-gray-500">
            Get notifications about your companies performance pushed to your preferred channel
          </p>
          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 border-b">
            <div class="col-span-1">

            </div>
            <div class="col-span-1 text-sm font-medium text-gray-500">
              Slack
            </div>
            <div class="col-span-1 text-sm font-medium text-gray-500">
              Email
            </div>
          </div>
          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 border-b">
            <div class="text-sm font-medium text-gray-500">
              Weekly
            </div>
            <div>
              <Switch v-model="storeState.settings.notifications.weekly.slack" :class="[storeState.settings.notifications.weekly.slack ? 'bg-indigo-600' : 'bg-gray-200', 'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500']">
                <span :class="[storeState.settings.notifications.weekly.slack ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none relative inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']">
                  <span :class="[storeState.settings.notifications.weekly.slack ? 'opacity-0 ease-out duration-100' : 'opacity-100 ease-in duration-200', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                    <svg class="h-3 w-3 text-gray-400" fill="none" viewBox="0 0 12 12">
                      <path d="M4 8l2-2m0 0l2-2M6 6L4 4m2 2l2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                  </span>
                  <span :class="[storeState.settings.notifications.weekly.slack ? 'opacity-100 ease-in duration-200' : 'opacity-0 ease-out duration-100', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                    <svg class="h-3 w-3 text-indigo-600" fill="currentColor" viewBox="0 0 12 12">
                      <path d="M3.707 5.293a1 1 0 00-1.414 1.414l1.414-1.414zM5 8l-.707.707a1 1 0 001.414 0L5 8zm4.707-3.293a1 1 0 00-1.414-1.414l1.414 1.414zm-7.414 2l2 2 1.414-1.414-2-2-1.414 1.414zm3.414 2l4-4-1.414-1.414-4 4 1.414 1.414z" />
                    </svg>
                  </span>
                </span>
              </Switch>
            </div>
            <div>
              <Switch v-model="storeState.settings.notifications.weekly.email" :class="[storeState.settings.notifications.weekly.email ? 'bg-indigo-600' : 'bg-gray-200', 'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500']">
                <span :class="[storeState.settings.notifications.weekly.email ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none relative inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']">
                  <span :class="[storeState.settings.notifications.weekly.email ? 'opacity-0 ease-out duration-100' : 'opacity-100 ease-in duration-200', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                    <svg class="h-3 w-3 text-gray-400" fill="none" viewBox="0 0 12 12">
                      <path d="M4 8l2-2m0 0l2-2M6 6L4 4m2 2l2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                  </span>
                  <span :class="[storeState.settings.notifications.weekly.email ? 'opacity-100 ease-in duration-200' : 'opacity-0 ease-out duration-100', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                    <svg class="h-3 w-3 text-indigo-600" fill="currentColor" viewBox="0 0 12 12">
                      <path d="M3.707 5.293a1 1 0 00-1.414 1.414l1.414-1.414zM5 8l-.707.707a1 1 0 001.414 0L5 8zm4.707-3.293a1 1 0 00-1.414-1.414l1.414 1.414zm-7.414 2l2 2 1.414-1.414-2-2-1.414 1.414zm3.414 2l4-4-1.414-1.414-4 4 1.414 1.414z" />
                    </svg>
                  </span>
                </span>
              </Switch>
            </div>
          </div>
          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 border-b">
            <div class="text-sm font-medium text-gray-500">
              Monthly
            </div>
            <div>
              <Switch v-model="storeState.settings.notifications.monthly.slack" :class="[storeState.settings.notifications.monthly.slack ? 'bg-indigo-600' : 'bg-gray-200', 'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500']">
                <span :class="[storeState.settings.notifications.monthly.slack ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none relative inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']">
                  <span :class="[storeState.settings.notifications.monthly.slack ? 'opacity-0 ease-out duration-100' : 'opacity-100 ease-in duration-200', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                    <svg class="h-3 w-3 text-gray-400" fill="none" viewBox="0 0 12 12">
                      <path d="M4 8l2-2m0 0l2-2M6 6L4 4m2 2l2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                  </span>
                  <span :class="[storeState.settings.notifications.monthly.slack ? 'opacity-100 ease-in duration-200' : 'opacity-0 ease-out duration-100', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                    <svg class="h-3 w-3 text-indigo-600" fill="currentColor" viewBox="0 0 12 12">
                      <path d="M3.707 5.293a1 1 0 00-1.414 1.414l1.414-1.414zM5 8l-.707.707a1 1 0 001.414 0L5 8zm4.707-3.293a1 1 0 00-1.414-1.414l1.414 1.414zm-7.414 2l2 2 1.414-1.414-2-2-1.414 1.414zm3.414 2l4-4-1.414-1.414-4 4 1.414 1.414z" />
                    </svg>
                  </span>
                </span>
              </Switch>
            </div>
            <div>
              <Switch v-model="storeState.settings.notifications.monthly.email" :class="[storeState.settings.notifications.monthly.email ? 'bg-indigo-600' : 'bg-gray-200', 'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500']">
                <span :class="[storeState.settings.notifications.monthly.email ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none relative inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']">
                  <span :class="[storeState.settings.notifications.monthly.email ? 'opacity-0 ease-out duration-100' : 'opacity-100 ease-in duration-200', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                    <svg class="h-3 w-3 text-gray-400" fill="none" viewBox="0 0 12 12">
                      <path d="M4 8l2-2m0 0l2-2M6 6L4 4m2 2l2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                  </span>
                  <span :class="[storeState.settings.notifications.monthly.email ? 'opacity-100 ease-in duration-200' : 'opacity-0 ease-out duration-100', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                    <svg class="h-3 w-3 text-indigo-600" fill="currentColor" viewBox="0 0 12 12">
                      <path d="M3.707 5.293a1 1 0 00-1.414 1.414l1.414-1.414zM5 8l-.707.707a1 1 0 001.414 0L5 8zm4.707-3.293a1 1 0 00-1.414-1.414l1.414 1.414zm-7.414 2l2 2 1.414-1.414-2-2-1.414 1.414zm3.414 2l4-4-1.414-1.414-4 4 1.414 1.414z" />
                    </svg>
                  </span>
                </span>
              </Switch>
            </div>
          </div>
        </div>
        <div class="pt-8">
          <div class="font-medium leading-6 text-gray-900 text-lg">
            Stripe
          </div>
          <p class="max-w-2xl text-sm text-gray-500">
            Import your Stripe data
          </p>
          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4">
            <div class="col-span-6 sm:col-span-2">
              <label for="stripe_api_key" class="block text-sm font-medium text-gray-700">API Key</label>
              <input 
                type="password" 
                v-model="stripeApiKey"
                name="stripe_api_key" 
                id="stripe_api_key" 
                autocomplete="password" 
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-gray-900 focus:border-gray-900 sm:text-sm" 
              />
            </div>
            <div class="col-span-6 sm:col-span-2">
              <button 
                @click="updateStripeApiKey"
                class="py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 shadow-sm hover:bg-indigo-500 focus:outline-none focus:shadow-outline-blue focus:bg-indigo-500 active:bg-indigo-600 transition duration-150 ease-in-out"
              >
                Update API Key
              </button>
            </div>
          </div>
        </div>
        <div class="pt-8">
          <div class="font-medium leading-6 text-gray-900 text-lg">
            Data model
          </div>
          <p class="max-w-2xl text-sm text-gray-500">
            Manually trigger your data model to update (this may take a few minutes)
          </p>
          <div class="pt-8">
            <button 
              @click="runDbt"
              :disabled="runningDbt"
              class="py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 shadow-sm hover:bg-indigo-500 focus:outline-none focus:shadow-outline-blue focus:bg-indigo-500 active:bg-indigo-600 transition duration-150 ease-in-out"
              :class="{
                'opacity-50': runningDbt, 
                'cursor-not-allowed': runningDbt
                }"
            >
              Refresh Data
            </button>
          </div>
        </div>
        
      </div>
      <div class="pt-16">
        storeState.settings: {{storeState.settings}}
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable no-unused-vars */
/* eslint-disable no-empty */
/* eslint-disable vue/no-unused-components */
import { store } from '../store.js';
import { reactive, ref } from 'vue'
// import { Switch, SwitchGroup, SwitchLabel } from '@headlessui/vue'
import { Listbox, ListboxButton, ListboxLabel, ListboxOption, ListboxOptions, Switch } from '@headlessui/vue'
import axios from 'axios';
import * as vega from "vega";
// import embed from 'vega-embed';
// import * as embed from "vega-embed";
// embed = require('vega-embed')
import Mousetrap from 'mousetrap'
import SSF from 'ssf'
// import PaperSelect from '@/components/PaperSelect.vue'

import { Grid, html } from "gridjs";
import "gridjs/dist/theme/mermaid.css";

import { 
  ArrowSmUpIcon, 
  ArrowSmDownIcon, 
  SearchIcon, 
  XIcon, 
  CheckCircleIcon,
  ExclamationCircleIcon,
  PlayIcon,
  // ChartBarIcon,
  // PresentationChartLineIcon,
  // ViewGridIcon,
  CheckIcon,
  SelectorIcon,
  } from '@heroicons/vue/solid'

import { 
  ChartBarIcon,
  ViewGridIcon,
  PresentationChartLineIcon,
  PresentationChartBarIcon,
  } from '@heroicons/vue/outline'

export default {
  name: 'Metrics',
  props: {
      msg: String
  },
  components: {
    SearchIcon,
    XIcon,
    CheckCircleIcon,
    ExclamationCircleIcon,
    PlayIcon,
    ChartBarIcon,
    PresentationChartLineIcon,
    PresentationChartBarIcon,
    ViewGridIcon,
    Listbox,
    ListboxButton,
    ListboxLabel,
    ListboxOption,
    ListboxOptions,
    Switch,
    CheckIcon,
    SelectorIcon,
  },
  created() {
    this.setupMousetrap()
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
    window.analyzeGrid = new Grid({
      sort: true,
      search: false,
      pagination: {
        limit: 20
      },
      fixedHeader: true,
      height: '400px',
      // columns: ["Name", "Email", "Phone Number"],
      data: [],
      className: {
        td: 'px-6 py-4 whitespace-nowrap text-sm text-gray-900 divide-y divide-gray-200',
        th: 'px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 tracking-wider',
        table: 'min-w-full divide-gray-200',
        tbody: 'bg-white '
      }
    })
    // window.vegaEmbed('#view', yourVlSpec);
  },
  mounted() {
    this.getDbt()
    // this.startTyped()
  },
  data() {
      return {
        store: store,
        storeState: store.state,
        stripeApiKey: '',
        runningDbt: false,
        analysisChanged: false,
        searchTerm: '',
        searching: true,
        running: false,
        updatingField: false,
        gotMetrics: false,
        gotDbt: false,
        fieldInUpdate: {},
        tableFilters: {
          active: false,
        },
        vizOptions: {
          axis: [
            { id: 1, value: 'none', label: 'None' },
            { id: 2, value: 'x', label: 'X-Axis' },
            { id: 3, value: 'y', label: 'Y-Axis' },
          ]
        },
        metricData: [],
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
          "title": {
            "font": "Inter, sans-serif",
            "fontSize": 14,
            "fontWeight": "bold",
            "dy": -3,
            "anchor": "start"
          },
          "axis": {
            "gridColor": "#ccc",
            "tickColor": "#fff",
            "domain": false,
            "grid": false
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
            "stroke": "#010101",
            "point": {"color": "#010101"},
            },
          "encoding": {
              "x": {
                "field": "month_dt", 
                "timeUnit": "yearmonth", 
                "title": null,
                // "axis": {"tickCount": {"interval": "month", "step": 6}}
                "axis": {
                  "values": [
                    {"year": 2019, "month": "may", "date": 1},
                    {"year": 2021, "month": "may", "date": 1}
                    ]
                  }
                },
              "y": {
                "field": "mrr", 
                "aggregate": "sum", 
                "type": "quantitative",
                "title": null
                },
              "tooltip": [
                  {"field": "month_dt", "timeUnit": "yearmonth", "title": "Date"},
                  {
                    "field": "mrr", 
                    "aggregate": "sum", 
                    "type": "quantitative",
                    "format": "$,.0f",
                    "title": "MRR"
                  }
              ]
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
    updateStripeApiKey() {
      const path = this.getApiUrl('update_secret')
      let d = {
        user: this.storeState.user, 
        stripeApiKey: this.stripeApiKey,
        type: 'stripe'
        }
      axios.post(path, d)
        .then((res) => {
          console.log('got update_secret: ', res.data)
        })
        .catch((error) => {
          console.error(error)
        })
    },
    runDbt() {
      if (!this.storeState.isLoggedIn || !this.storeState.gotUserData) return
      this.runningDbt = true
      const path = this.getApiUrl('run_dbt')
      let d = {user: this.storeState.user, userData: this.storeState.userData}
      axios.post(path, d)
        .then((res) => {
          this.runningDbt = false
          console.log('got run_dbt: ', res.data)
        })
        .catch((error) => {
          this.runningDbt = false
          console.error(error)
        })
    },
    updateDimensionNow(index, index2, column) {
      this.updatingField = true
      this.fieldInUpdate = column
      this.fieldInUpdate.index = index
      this.fieldInUpdate.index2 = index2
      this.fieldInUpdate.dimOrMeas = 'dimension'
      let label = this.getDimensionLabel(column)
      if (this.storeState.analysis.viz.encoding.x.field === label) {
        this.fieldInUpdate.axis = this.vizOptions.axis[1]
      }
      if (this.storeState.analysis.viz.encoding.y.field === label) {
        this.fieldInUpdate.axis = this.vizOptions.axis[2]
      }
      if (!this.fieldInUpdate.axis) this.fieldInUpdate.axis = this.vizOptions.axis[0]
    },
    updateMeasureNow(index, index3, measureName) {
      let model = this.storeState.dbt.models[index]
      let column = model.columns[index3]
      
      let measure = this.storeState.dbt.models[index].columns[index3].meta.measures[measureName]
      this.fieldInUpdate = measure
      this.fieldInUpdate.description = `${measure.type} of ${model.name}.${column.name}`
      // this.fieldInUpdate.column = column
      this.updatingField = true
      this.fieldInUpdate.index = index
      this.fieldInUpdate.index3 = index3
      this.fieldInUpdate.dimOrMeas = 'measure'
      let label = this.getMeasureLabel(measure)
      if (this.storeState.analysis.viz.encoding.x.field === label) {
        this.fieldInUpdate.axis = this.vizOptions.axis[1]
      }
      if (this.storeState.analysis.viz.encoding.y.field === label) {
        this.fieldInUpdate.axis = this.vizOptions.axis[2]
      }
      if (!this.fieldInUpdate.axis) this.fieldInUpdate.axis = this.vizOptions.axis[0]
    },
    flipVizType(type) {
      this.storeState.analysis.viz.type = type
      this.createViz({})
    },
    createViz(opts) {
      console.log('createViz...')
      this.searching = false
      this.updatingField = false
      this.searchTerm = ''
      if (this.storeState.analysis.results.rows.length === 0) return
      let vegaOpts = {
        config: this.vegaConfig,
        actions: false,
      }
      let viz = this.deepCopy(this.vegaSpec)
      viz.encoding = this.storeState.analysis.viz.encoding
      viz.encoding.tooltip = []
      if (viz.encoding.x.field) {
        let ttX = {"field": viz.encoding.x.field, "title": viz.encoding.x.field}
        viz.encoding.tooltip.push(ttX)
      }
      if (viz.encoding.y.field) {
        let ttY = {"field": viz.encoding.y.field, "title": viz.encoding.y.field}
        viz.encoding.tooltip.push(ttY)
      }
      
//       {
//     "x": {
//         "field": "Month",
//         "type": "ordinal"
//     },
//     "y": {
//         "field": "Avg MRR",
//         "type": "quantitative"
//     }
// }
      // customers.encoding.tooltip = [
      //     {"field": "mrr_month_dt", "timeUnit": "yearmonth", "title": "Date"},
      //     {
      //       "field": "active", 
      //       "aggregate": "sum", 
      //       "type": "quantitative",
      //       "format": ",.0f",
      //       "title": "Customers"
      //     }
      // ]
      viz.mark.type = this.storeState.analysis.viz.type
      // viz.data.values = []
      for (let index = 0; index < this.storeState.analysis.results.rows.length; index++) {
        let row = {}
        const element = this.storeState.analysis.results.rows[index];
        for (let index2 = 0; index2 < this.storeState.analysis.results.cols.length; index2++) {
          row[this.storeState.analysis.results.cols[index2].name] = element[index2]
        }
        viz.data.values.push(row)
      }
      window.vegaEmbed('#viz', viz, opts);
    },
    setupMousetrap() {
      var self = this
      Mousetrap.bind('4', function(e) { console.log('4'); });
      Mousetrap.bind('/', function(e) { 
        if (e && e.preventDefault) e.preventDefault()
        self.$refs.search.focus()
      });
      Mousetrap.bind('esc', function(e) { 
        if (e && e.preventDefault) e.preventDefault()
        self.$refs.search.blur()
        self.searching = false
        self.updatingField = false
        self.searchTerm = ''
      });
      Mousetrap.bind('command+enter', function(e) { 
        if (e && e.preventDefault) e.preventDefault()
        self.runAnalysis()
      });
      
    },
    closeSearch() {
      this.$refs.search.blur()
      this.searching = false
      this.searchTerm = ''
    },
    generateDemoTable() {
      new Grid({
        sort: true,
        // search: true,
        columns: ["Name", "Email", "Phone Number"],
        data: [
          ["John", "john@example.com", "(353) 01 222 3333"],
          ["Mark", "mark@gmail.com", "(01) 22 888 4444"],
          ["Eoin", "eoin@gmail.com", "0097 22 654 00033"],
          ["Sarah", "sarahcdd@gmail.com", "+322 876 1233"],
          ["Afshin", "afshin@mail.com", "(353) 22 87 8356"]
        ],
        className: {
          td: 'px-6 py-4 whitespace-nowrap text-sm text-gray-900 divide-y divide-gray-200',
          th: 'px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider',
          table: 'min-w-full divide-gray-200',
          tbody: 'bg-white '
        }
      }).render(document.getElementById("testtable"));
    },
    createGrid(data) {
      console.log('createGrid...')
  //     columns: [
  //     { 
  //       name: 'Name',
  //       formatter: (cell) => `Name: ${cell}`
  //     },
  //     'Email',
  //  ],
      let columns = []
      for (let index = 0; index < data.cols.length; index++) {
        const col = data.cols[index];
        if (col.format) col.formatter = (cell) => `${SSF.format(col.format, cell)}`
        // col.formatter = (cell) => `${col.format}: ${cell}`
        columns.push(col)
      }
      window.analyzeGrid.updateConfig({
      // lets update the columns field only
        data: data.rows,
        columns: columns
      })
      if (window.analyzeGrid.config.container) {
        window.analyzeGrid.forceRender()
      } else {
        window.analyzeGrid.render(document.getElementById("gridInner"));
      }
      // document.getElementById("customerTable").innerHTML = ''
    },
    getApiUrl(endpoint) {
      if (process.env.NODE_ENV != 'production') return `http://127.0.0.1:5000/${endpoint}`
      return `https://paperapi.onrender.com/${endpoint}`
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
    moreInfo(row) {
      // this.saveFunder(row)
      if (!this.storeState.isLoggedIn || !this.storeState.user.publicAddress) {
        this.$router.push({ name: 'Login', query: { goto: 'Landing' }})
      } else {
        let url = `http://${row.domain}/?ref=trypaperio`
        window.open(url, '_blank');
      }
    },
    searchMatch(model, column) {
      if (this.searchTerm.length === 0) return true
      // var searchIn = `${model.name} ${column.name}`
      var searchIn = `${column.name}`
      let label = this.getLabel(column)
      if (label) searchIn += ` ${label}`
      if (searchIn.includes(this.searchTerm)) return true
      return false
    },
    selectColumnTimeframe(index, index2, column, timeframe) {
      let dimOrMeas = 'dimension'
      let curVal = this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].timeframe
      if (curVal === timeframe) {
        this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].timeframe = false
        this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].selected = false
      } else {
        this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].timeframe = timeframe
        this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].selected = true
      }
      this.searchTerm = ''
    },
    removeColumn(index, index2, column, dimOrMeas) {
      if (this.isDateColumn(column)) {
        this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].timeframe = false
        this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].selected = false
        return
      }
      let curVal = this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].selected
      this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].selected = !curVal
      this.searchTerm = ''
      var self = this
      setTimeout(() => self.updatingField = false, 0);
      // this.$nextTick(function() {
      //   // DOM is now updated
      //   // `this` is bound to the current instance
      //   console.log('removeColumn: ', column)
      //   this.updatingField = false
      // })
    },
    selectColumn(index, index2, column, dimOrMeas) {
      if (this.isDateColumn(column)) {
        return
      }
      let curVal = this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].selected
      this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].selected = !curVal
      this.searchTerm = ''
    },
    selectMeasure(index, index2, measureName) {
      let curVal = this.storeState.dbt.models[index].columns[index2].meta.measures[measureName].selected
      this.storeState.dbt.models[index].columns[index2].meta.measures[measureName].selected = !curVal
      this.searchTerm = ''
      this.$forceUpdate()
      setTimeout(() => this.updatingField = false, 0);
    },
    isMeasureSelected(index, index2, measureName) {
      let curVal = this.storeState.dbt.models[index].columns[index2].meta.measures[measureName].selected
      return curVal
    },
    isDimOrMeas(index, index2, column, dimOrMeas) {
      let exists = this.storeState.dbt.models[index].columns.find(c => c.name === column.name)
      return exists.meta && exists.meta[dimOrMeas]
    },
    isDateColumn(column) {
      return column.meta && column.meta.dimension && column.meta.dimension.timeframes
    },
    isSelected(index, index2, column, dimOrMeas) {
      if (this.storeState.dbt.models[index].columns[index2] && 
          this.storeState.dbt.models[index].columns[index2].meta && 
          this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas]
          ) {
            return this.storeState.dbt.models[index].columns[index2].meta[dimOrMeas].selected
          }
      return false
    },
    getFieldLabel(fieldInUpdate) {
      if (fieldInUpdate.dimOrMeas === 'measure') {
        return fieldInUpdate.label
      }
      return this.getDimensionLabel(fieldInUpdate)
    },
    getLabel(column) {
      if (column.meta && column.meta.dimension && column.meta.dimension.label) {
        return column.meta.dimension.label
      } else if (column.meta && column.meta.measure && column.meta.measure.label) {
        return column.meta.measure.label
      }
      return false
    },
    getDimensionLabel(column) {
      if (column.meta && column.meta.dimension && column.meta.dimension.label) {
        return column.meta.dimension.label
      }
      return column.name
    },
    getMeasureLabel(column, columnName) {
      if (column && column.label) {
        return column.label
      }
      return columnName
    },
    getSelected(column) {
      if (column.meta && column.meta.dimension && column.meta.dimension.label) {
        return column.meta.dimension.label
      }
      if (column.meta && column.meta.measure && column.meta.measure.label) {
        return column.meta.measure.label
      }
      return column.name
    },
    getDbt() {
      this.gotDbt = false
      const path = this.getApiUrl('get_dbt')
      let d = {user: this.storeState.user, userData: this.storeState.userData}
      axios.post(path, d)
        .then((res) => {
          console.log('got get_dbt: ', res.data)
          this.gotDbt = true
          this.storeState.dbt = res.data.data
          // this.metricData = reactive(res.data)
          // this.createCharts()
          // this.createCustomerTable()
        })
        .catch((error) => {
          console.error(error)
        })
    },
    cancelRun() {
      this.running = false
      this.searching = false
    },
    getAllSelected() {
      let selected = []
      for (let index = 0; index < this.storeState.dbt.models.length; index++) {
        const model = this.storeState.dbt.models[index]
        if (!model.columns) continue
        for (let index2 = 0; index2 < model.columns.length; index2++) {
          const col = model.columns[index2]
          var measures = col && col.meta && col.meta.measures
          if (measures) {
            for (const [key, measure] of Object.entries(measures)) {
              if (measure.selected) {
                measure.dimOrMeas = 'measure'
                selected.push(measure)
              }
            }
          }
          var dimension = col && col.meta && col.meta.dimension
          if (dimension && dimension.selected) {
            dimension.dimOrMeas = 'dimension'
            selected.push(dimension)
          }
        }
      }
      return selected
    },
    showMsg(self, opts) {
      self.storeState.msg.show = true
      self.storeState.msg.primary = opts.primary
      self.storeState.msg.secondary = opts.secondary
      self.storeState.msg.type = opts.type
      setTimeout(() => self.storeState.msg.show = false, self.storeState.msg.time);
    },
    runAnalysis() {
      console.log('runAnalysis...')
      let selected = this.getAllSelected()
      this.analysisChanged = false
      if (selected.length === 0) {
        this.searching = true
        let opts = {
          primary: 'Error running analysis',
          secondary: 'You need to select at least one dimension or measure.',
          type: 'error'
          }
        this.showMsg(this, opts)
        return
      }
      const path = this.getApiUrl('run_analysis')
      let d = {user: this.storeState.user, dbt: this.storeState.dbt}
      this.running = true
      this.searching = false
      axios.post(path, d)
        .then((res) => {
          this.running = false
          if (!res.data.ok) {
            console.error(res)
            let opts = {
              primary: 'Error running analysis',
              secondary: res.data.error,
              }
            this.showMsg(this, opts)
            return
          }
          console.log('runAnalysis: ', res.data)
          
          this.storeState.analysis.results = res.data
          this.createGrid(res.data)
          if (!this.storeState.analysis.viz.encoding.x.field) {
            for (let index = 0; index < res.data.sql.selected.length; index++) {
              const selected = res.data.sql.selected[index];
              if (selected.dimOrMeas === 'dimension') {
                this.storeState.analysis.viz.encoding.x.field = selected.alias
                break
              }
            } 
          }
          if (!this.storeState.analysis.viz.encoding.y.field) {
            for (let index = 0; index < res.data.sql.selected.length; index++) {
              const selected = res.data.sql.selected[index];
              if (selected.dimOrMeas === 'measure') {
                this.storeState.analysis.viz.encoding.y.field = selected.alias
                break
              }
            } 
          }
          this.createViz({})
          // this.getAllSelected()
          // this.metricData = reactive(res.data)
          // this.createCharts()
          // this.createCustomerTable()
        })
        .catch((error) => {
          this.running = false
          console.error(error)
        })
    },
    getMetrics() {
      this.gotMetrics = false
      const path = this.getApiUrl('get_metrics')
      let d = {user: this.storeState.user, userData: this.storeState.userData}
      axios.post(path, d)
        .then((res) => {
          console.log('got get_metrics: ', res.data)
          this.gotMetrics = true
          this.metricData = reactive(res.data)
          // this.createCharts()
          // this.createCustomerTable()
        })
        .catch((error) => {
          console.error(error)
        })
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
    formatMoney(m) {
      return (m / 1000).toFixed(1)
    },
  },
  watch: {
    'tableFilters': {
        handler: function () {
          this.createCustomerTable()
        },
        deep: true
    },
    'fieldInUpdate': {
      handler: function () {
        if (this.fieldInUpdate.axis && this.fieldInUpdate.axis.value != 'none') {
          let axis = this.fieldInUpdate.axis.value
          let label = this.getFieldLabel(this.fieldInUpdate)
          this.storeState.analysis.viz.encoding[axis].field = label
          this.createViz({})
        }
        
      },
      deep: true
    },
    'storeState.dbt.models': {
      handler: function () {
        let selected = this.getAllSelected()
        if (selected.length > 0) this.analysisChanged = true
        
      },
      deep: true
    }
  },
}
/* eslint-disable no-unused-vars */
/* eslint-disable no-empty */
/* eslint-disable vue/no-unused-components */

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
  .gridjs-tbody {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
    line-height: 1.5;
    --border-opacity: 1;
    border-collapse: collapse;
    box-sizing: border-box;
    border-width: 1px !important;
    border-style: solid;
    --bg-opacity: 1;
    background-color: rgba(255, 255, 255, var(--bg-opacity));
    --divide-opacity: 1;
    border-color: rgba(237, 242, 247, var(--divide-opacity));
  }
</style>
