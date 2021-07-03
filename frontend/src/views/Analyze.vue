<template>
  <div>
    <div v-if="!storeState.gotDbt">
      <div class="flex justify-center space-y-8 w-full pt-32">
        <svg class="animate-spin -ml-1 mr-3 h-20 w-20 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>
    </div>
    <div v-else class="px-8 py-4">
      <div class="flex-1 flex">
        <div class="w-full flex md:ml-0">
          <div class="relative w-full text-gray-400 focus-within:text-gray-600">
            <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center">
              <SearchIcon class="flex-shrink-0 h-5 w-5" aria-hidden="true" />
            </div>
            <input 
              v-model="searchTerm"
              ref="search"
              name="search_field" 
              id="search_field" 
              class="mousetrap h-full w-full border-transparent py-2 pl-8 pr-3 text-base text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-0 focus:border-transparent focus:placeholder-gray-400" 
              placeholder="Search" 
              autocomplete="off"
              @focus="searching = true"
            />
          </div>
        </div>
        <div 
          v-if="!running" @click="runAnalysis" 
          class="text-indigo-700 hover:text-indigo-400 cursor-pointer"
          :class="{'animate-pulse': analysisChanged}"
        >
          <PlayIcon class="flex-shrink-0 h-10 w-10" aria-hidden="true" />
        </div>
        <!-- <div v-else-if="searching" @click="closeSearch" class="text-gray-400 hover:text-gray-700 cursor-pointer">
          <XIcon class="flex-shrink-0 h-8 w-8" aria-hidden="true" />
        </div> -->
        <div class="flex" v-else>
          <div class="mr-4 mt-1 font-bold hover:text-gray-500 text-gray-900 rounded cursor-pointer" @click="cancelRun">
            Cancel
          </div>
          <svg class="animate-spin h-8 w-8 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
      </div>
      <div class="grid grid-cols-12 pt-4">
        <div
          v-if="updatingField"
          class="col-span-9"
        >
          <div class="text-xl font-bold">
            {{getFieldLabel(fieldInUpdate)}}
          </div>
          <div class="text-gray-500">
            {{fieldInUpdate.description}}
          </div>
          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 border-t border-b mt-4">
            <dt class="text-sm font-medium text-gray-500">
              Filter
            </dt>
            <dd class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              <span class="ml-4 flex-shrink-0">
                <button type="button" class="bg-white rounded-md font-medium text-purple-600 hover:text-purple-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500">
                  Add
                </button>
              </span>
            </dd>
          </div>
          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 border-b">
            <dt class="text-sm font-medium text-gray-500">
              Axis
            </dt>
            <dd class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              <div>
                <Listbox as="div" v-model="fieldInUpdate.axis">
                  <div class="mt-1 relative">
                    <ListboxButton class="bg-white relative w-full border border-gray-300 rounded-md shadow-sm pl-3 pr-10 py-2 text-left cursor-default focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                      <span class="block truncate">{{ fieldInUpdate.axis.label }}</span>
                      <span class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                        <SelectorIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                      </span>
                    </ListboxButton>

                    <transition leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100" leave-to-class="opacity-0">
                      <ListboxOptions class="absolute z-10 mt-1 w-full bg-white shadow-lg max-h-60 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm">
                        <ListboxOption 
                          as="template" 
                          v-for="(option, index) in vizOptions.axis" 
                          :key="index" 
                          :value="option" 
                          v-slot="{ active, selected }"
                        >
                          <li :class="[active ? 'text-white bg-indigo-600' : 'text-gray-900', 'cursor-default select-none relative py-2 pl-3 pr-9']">
                            <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">
                              {{ option.label }} 
                              <!-- {{selected}} {{active}} -->
                            </span>

                            <span v-if="selected" :class="[selected ? 'text-white' : 'text-indigo-600', 'absolute inset-y-0 right-0 flex items-center pr-4']">
                              <CheckIcon class="h-5 w-5" aria-hidden="true" />
                              
                            </span>
                          </li>
                        </ListboxOption>
                      </ListboxOptions>
                    </transition>
                  </div>
                </Listbox>
              </div>
            </dd>
          </div>
          <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 border-b">
            <dt class="text-sm font-medium text-gray-500">
              Hidden
            </dt>
            <dd class="mt-1 flex text-sm text-gray-900 sm:mt-0 sm:col-span-2">
              <div>
                <Switch v-model="fieldInUpdate.hidden" :class="[fieldInUpdate.hidden ? 'bg-indigo-600' : 'bg-gray-200', 'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500']">
                  <span class="sr-only">Use setting</span>
                  <span :class="[fieldInUpdate.hidden ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none relative inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']">
                    <span :class="[fieldInUpdate.hidden ? 'opacity-0 ease-out duration-100' : 'opacity-100 ease-in duration-200', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                      <svg class="h-3 w-3 text-gray-400" fill="none" viewBox="0 0 12 12">
                        <path d="M4 8l2-2m0 0l2-2M6 6L4 4m2 2l2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                      </svg>
                    </span>
                    <span :class="[fieldInUpdate.hidden ? 'opacity-100 ease-in duration-200' : 'opacity-0 ease-out duration-100', 'absolute inset-0 h-full w-full flex items-center justify-center transition-opacity']" aria-hidden="true">
                      <svg class="h-3 w-3 text-indigo-600" fill="currentColor" viewBox="0 0 12 12">
                        <path d="M3.707 5.293a1 1 0 00-1.414 1.414l1.414-1.414zM5 8l-.707.707a1 1 0 001.414 0L5 8zm4.707-3.293a1 1 0 00-1.414-1.414l1.414 1.414zm-7.414 2l2 2 1.414-1.414-2-2-1.414 1.414zm3.414 2l4-4-1.414-1.414-4 4 1.414 1.414z" />
                      </svg>
                    </span>
                  </span>
                </Switch>
              </div>
            </dd>
          </div>
          <div class="grid grid-cols-12 pt-4">
            <div class="col-span-9"></div>
            <div class="col-span-3">
              <div>
                <button 
                  @click="updatingField=false"
                  class="w-full py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 shadow-sm hover:bg-indigo-500 focus:outline-none focus:shadow-outline-blue focus:bg-indigo-500 active:bg-indigo-600 transition duration-150 ease-in-out"
                >
                  Done
                </button>
              </div>
              
            </div>
          </div>
          <!-- <div>
            fieldInUpdate: {{fieldInUpdate}}
          </div>
          <div>
            storeState.analysis.viz: {{storeState.analysis.viz}}
          </div> -->
        </div>
        <div class="col-span-9 pt-4" v-else>
          <span
            v-for="(model, index) in storeState.dbt.models"
            :key="index"
          >
            <span
              v-for="(column, index2) in model.columns"
              :key="index2"
            >
              <span 
                v-if="isSelected(index, index2, column, 'dimension')"
              >
                <span @click="updateDimensionNow(index, index2, column)" class="mr-3 mb-2 inline-flex rounded cursor-pointer items-center py-1 pl-3 pr-1 text-sm font-medium bg-indigo-100 text-indigo-700">
                  {{model.name}}.{{getDimensionLabel(column)}}
                  <button @click="removeColumn(index, index2, column, 'dimension')" type="button" class="flex-shrink-0 ml-1 h-4 w-4 rounded-full inline-flex items-center justify-center text-indigo-400 hover:bg-indigo-200 hover:text-indigo-500 focus:outline-none focus:bg-indigo-500 focus:text-white">
                    <svg class="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
                      <path stroke-linecap="round" stroke-width="1.5" d="M1 1l6 6m0-6L1 7" />
                    </svg>
                  </button>
                </span>
              </span>
            </span>
            <span
              v-for="(column, index3) in model.columns"
              :key="index3"
            >
              <span 
                v-if="isDimOrMeas(index, index3, column, 'measures')"
              >
                <span
                  v-for="(measure, measureName, index4) in model.columns[index3].meta.measures"
                  :key="index4"
                >
                  <span 
                    v-if="isMeasureSelected(index, index3, measureName)"
                  >
                    <span @click="updateMeasureNow(index, index3, measureName, column)" class="mr-3 mb-2 inline-flex rounded cursor-pointer items-center py-1 pl-3 pr-1 text-sm font-medium bg-indigo-100 text-indigo-700">
                      {{model.name}}.{{getMeasureLabel(measure, measureName)}}
                      <button @click="selectMeasure(index, index3, measureName)" type="button" class="flex-shrink-0 ml-1 h-4 w-4 rounded-full inline-flex items-center justify-center text-indigo-400 hover:bg-indigo-200 hover:text-indigo-500 focus:outline-none focus:bg-indigo-500 focus:text-white">
                        <svg class="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
                          <path stroke-linecap="round" stroke-width="1.5" d="M1 1l6 6m0-6L1 7" />
                        </svg>
                      </button>
                    </span>
                  </span>
                </span>
              </span>
            </span>
          </span>
        </div>
        <div class="col-span-3 pt-4 flex justify-end mr-2">
          <ViewGridIcon 
            class="h-6 w-6 hover:bg-gray-200 rounded cursor-pointer ml-3 text-gray-500"
            :class="{'text-gray-900': storeState.analysis.viz.type === 'grid'}"
            aria-hidden="true" 
            @click="flipVizType('grid')"
          />
          <PresentationChartLineIcon 
            class="h-6 w-6 hover:bg-gray-200 rounded cursor-pointer ml-3 text-gray-500"
            :class="{'text-gray-900': storeState.analysis.viz.type === 'line'}"
            aria-hidden="true" 
            @click="flipVizType('line')"
          />
          <PresentationChartBarIcon 
            class="h-6 w-6 hover:bg-gray-200 rounded cursor-pointer ml-3 text-gray-500"
            :class="{'text-gray-900': storeState.analysis.viz.type === 'bar'}"
            aria-hidden="true" 
            @click="flipVizType('bar')"
          />
          <!-- <ViewGridIcon 
            class="h-8 w-8 hover:bg-gray-200 rounded cursor-pointer ml-3" 
            aria-hidden="true" 
          /> -->
        </div>
      </div>
      <div 
        :class="{
          'hidden': !searching,
          'pt-4': true
        }"
      >
        <div class="float-right mr-2">
          <XIcon 
            class="flex-shrink-0 h-6 w-6 hover:bg-gray-200 rounded cursor-pointer" aria-hidden="true" 
            @click="searching=false"
          />
        </div>
        <div
          v-for="(model, index) in storeState.dbt.models"
          :key="index"
        >
          <div class="font-bold text-2xl">
            {{model.name}}
          </div>
          <div class="font-bold pl-4 border-l text-red-400">
            Dimensions
          </div>
          <div
            v-for="(column, index2) in model.columns"
            :key="index2"
            @click="selectColumn(index, index2, column, 'dimension')"
            class="border-l"
          >
            <div 
              v-if="isDimOrMeas(index, index2, column, 'dimension') && searchMatch(model, column)"
              :class="{
                'cursor-pointer': !isDateColumn(column),
                'hover:bg-gray-200': !isDateColumn(column),
                'text-red-400': true,
                'font-bold': isSelected(index, index2, column, 'dimension') && !isDateColumn(column),
                'rounded': true,
                'py-1': true, 
                'pl-4': true,
              }"
            >
              {{getDimensionLabel(column)}}
              <div v-if="isDateColumn(column)" class="font-normal cursor-pointer border-l">
                <div
                  v-for="(timeframe, index2b) in column.meta.dimension.timeframes"
                  :key="index2b"
                  @click="selectColumnTimeframe(index, index2, column, timeframe)"
                  :class="{
                    'font-bold': column.meta.dimension.timeframe === timeframe,
                    'pl-4': true,
                    'hover:bg-gray-200': true,
                    'rounded': true,
                    'py-1': true,
                  }"
                >
                  {{timeframe}}
                </div>
              </div>
            </div>
          </div>
          <div class="font-bold pl-4 border-l text-blue-400">
            Measures
          </div>
          <div
            v-for="(column, index3) in model.columns"
            :key="index3"
          >
            <div 
              v-if="isDimOrMeas(index, index3, column, 'measures') && searchMatch(model, column)"
              class="border-l"
            >
              <div
                v-for="(measure, measureName, index4) in model.columns[index3].meta.measures"
                :key="index4"
                @click="selectMeasure(index, index3, measureName)"
                :class="{
                  'cursor-pointer': true,
                  'hover:bg-gray-200': true,
                  'text-blue-400': true,
                  'rounded': true,
                  'font-bold': isMeasureSelected(index, index3, measureName),
                  'py-1': true, 
                  'pl-4': true,
                }"
              >
                {{getMeasureLabel(measure, measureName)}}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div 
      class="px-4 py-4 w-full"
      :class="{'hidden': storeState.analysis.viz.type === 'grid'}"
    >
      <div class="w-full" id="viz">
      </div>
    </div>
    <div 
      class="px-4 py-4"
      :class="{'hidden': storeState.analysis.viz.type != 'grid'}"
    >
      <div>
        <div id="gridInner">

        </div>
      </div>
    </div>
    <div>
      <!-- {{storeState.dbt}} -->
    </div>
    <div>
      <!-- {{storeState.analysis.results}} -->
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
      width: 'unset',
      // columns: ["Name", "Email", "Phone Number"],
      data: [],
      className: {
        td: 'px-6 py-4 whitespace-nowrap text-sm text-gray-900 divide-y divide-gray-200',
        th: 'px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 tracking-wider',
        table: 'min-w-full divide-gray-200 w-auto',
        tbody: 'bg-white '
      }
    })
    // window.vegaEmbed('#view', yourVlSpec);
  },
  mounted() {
    this.checkUrl()
    // this.getDbt()
    // this.startTyped()
  },
  data() {
      return {
        store: store,
        storeState: store.state,
        analysisChanged: false,
        searchTerm: '',
        searching: true,
        running: false,
        updatingField: false,
        gotMetrics: false,
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
          // "width": "500",
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
    checkUrl() {
      if (this.$route.query.table) {
        console.log('checkUrl', this.$route.query.table, this.storeState.dbt.models)
        if (this.storeState.dbt.models) {
          this.deselectAll()
          let table = this.storeState.dbt.models.findIndex(m => m.name === this.$route.query.table)
          if (table >= 0) {
            for (let index = 0; index < this.storeState.dbt.models[table].columns.length; index++) {
              this.storeState.dbt.models[table].columns[index].meta.dimension.selected = true 
            }
            this.runAnalysis()
          }
        }
      }
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
      console.log('createViz...', this.storeState.analysis.viz.type)
      if (this.storeState.analysis.viz.type === 'grid') {
        this.createGrid(false)
        return
      }
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
      if (!data) data = this.storeState.analysis.results
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
      } else if (document.getElementById("gridInner")) {
        window.analyzeGrid.render(document.getElementById("gridInner"));
      } else {
        console.error('no container for grid...')
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
    deselectAll() {
      for (let index = 0; index < this.storeState.dbt.models.length; index++) {
        const model = this.storeState.dbt.models[index]
        if (!model.columns) continue
        for (let index2 = 0; index2 < model.columns.length; index2++) {
          const col = model.columns[index2]
          var measures = col && col.meta && col.meta.measures
          if (measures) {
            for (const [key, measure] of Object.entries(measures)) {
              if (measure.selected) measure.selected = false
            }
          }
          var dimension = col && col.meta && col.meta.dimension
          if (dimension && dimension.selected) {
            dimension.selected = false
          }
        }
      }
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
              type: 'error'
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
          if (this.storeState.analysis.results.rows.length <= 100) this.createViz({})
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
