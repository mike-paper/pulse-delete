<template>
<!--
  This example requires Tailwind CSS v2.0+ 
  
  This example requires some changes to your config:
  
  ```
  // tailwind.config.js
  module.exports = {
    // ...
    plugins: [
      // ...
      require('@tailwindcss/forms'),
    ]
  }
  ```
-->
<div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
  <div v-if="!checkedIfLoggedIn" class="flex justify-center max-w-md space-y-8 w-full">
    <svg class="animate-spin -ml-1 mr-3 h-20 w-20 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
  </div>
  <div v-else class="max-w-md w-full space-y-8">
    <div>
      <img class="mx-auto h-12 w-auto" src="/paper-logo.png" alt="Paper">
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        Sign in to your account
      </h2>
      <!-- <p class="mt-2 text-center text-sm text-gray-600">
        Or
        <a href="#" class="font-medium text-indigo-600 hover:text-indigo-500">
          start your 14-day free trial
        </a>
      </p> -->
    </div>
    <div class="mt-8 space-y-6">
      <input type="hidden" name="remember" value="true">
      <div class="rounded-md shadow-sm -space-y-px">
        <div>
          <label for="email-address" class="sr-only">Email address</label>
          <input v-model="email" ref="email" id="email-address" name="email" type="email" autocomplete="email" required class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="Email address">
        </div>
        <!-- <div>
          <label for="password" class="sr-only">Password</label>
          <input id="password" name="password" type="password" autocomplete="current-password" required class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="Password">
        </div> -->
      </div>

      <div class="flex items-center justify-between">
        <div class="flex items-center">
          <input id="remember_me" name="remember_me" type="checkbox" class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded">
          <label for="remember_me" class="ml-2 block text-sm text-gray-900">
            Remember me
          </label>
        </div>

        <div class="text-sm">
          <a href="mailto:contact@trypaper.io" target="_blank" class="font-medium text-indigo-600 hover:text-indigo-500">
            Forgot your password?
          </a>
        </div>
      </div>

      <div>
        <button @click="handleLogin" class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
          <span class="absolute left-0 inset-y-0 flex items-center pl-3">
            <!-- Heroicon name: lock-closed -->
            <svg class="h-5 w-5 text-indigo-500 group-hover:text-indigo-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
            </svg>
          </span>
          Sign in
        </button>
      </div>
    </div>
    <div class="border-t-2 flex justify-center pt-8">
      <div class="-mt-12 absolute bg-white px-4 text-gray-500">or</div>
      <div class="cursor-pointer" @click="handleGoogleLogin">
        <img src="/sign-in-with-google.svg">
      </div>
    </div>
    
  </div>
</div>
</template>

<script>
/* eslint-disable no-unused-vars */
import axios from 'axios';
import { Magic } from 'magic-sdk';
import { OAuthExtension } from '@magic-ext/oauth';

import { store } from '../store.js';

const magic = new Magic('pk_live_7F06D4CDC50CBA64', {
  extensions: [new OAuthExtension()],
});
// magic.preload;




export default {
  name: 'Login',
  props: {
      msg: String
  },
  created() {
    this.render()
  },
  methods: {
    countryCodeEmoji(cc) {
      if (!cc) return ''
      if (!cc.geo) return ''
      if (!cc.geo.countryCode) return ''
      cc = cc.geo.countryCode
      const CC_REGEX = /^[a-z]{2}$/i;
      const OFFSET = 127397;
      if (!CC_REGEX.test(cc)) {
        const type = typeof cc;
        throw new TypeError(
          `cc argument must be an ISO 3166-1 alpha-2 string, but got '${
            type === 'string' ? cc : type
          }' instead.`,
        );
      }
      const chars = [...cc.toUpperCase()].map(c => c.charCodeAt() + OFFSET);
      return String.fromCodePoint(...chars);
    },
    async handleLogout() {
      await magic.user.logout();
      // this.render();
    },
    handleLogin(e) {
      // e.preventDefault();
      // const email = this.email
      if (this.email.length > 0) {
        // window.posthog.capture('login-attempt', {email: this.email});
        /* One-liner login 🤯 */
        magic.auth.loginWithMagicLink({ email: this.email }).then(
          p => this.render()
        )
        // this.render();
      } else {
        this.$refs.email.focus()
      }
    },
    async handleGoogleLogin(e) {
      // e.preventDefault();
      // const email = this.email
      // window.posthog.capture('login-attempt', {email: 'googleoauth'});
      /* One-liner login 🤯 */
      
      // await magic.oauth.loginWithRedirect({
      //   provider: 'google' /* 'google', 'facebook', 'apple', or 'github' */,
      //   redirectURI: redirectURI,
      //   // scopes: ['user:email'], /* optional */
      // });
      let redirectURI = this.getAppUrl('callback')
      magic.oauth.loginWithRedirect({
        provider: 'google' /* 'google', 'facebook', 'apple', or 'github' */,
        redirectURI: redirectURI,
        scopes: ['user:email'], /* optional */
      }).then(res => console.log('loginWithRedirect: ', res))
    },
    // handleLogin(e) {
    //   // e.preventDefault();
    //   // const email = this.email
    //   if (this.email) {
    //     /* One-liner login 🤯 */
    //     magic.auth.loginWithMagicLink({ email: this.email });
    //     this.render();
    //   }
    // },
    /* 3. Implement Render Function */
    async render() {
      this.checkedIfLoggedIn = false
      this.storeState.isLoggedIn = await magic.user.isLoggedIn();
      /* Show login form if user is not logged in */
      if (this.storeState.isLoggedIn) {
        /* Get user metadata including email */
        const userMetadata = await magic.user.getMetadata();
        this.storeState.user = userMetadata
        this.storeState.hideSidebar = false
        console.log('logged in...', userMetadata.email)
        const idToken = await magic.user.getIdToken();
        this.loginUser(userMetadata, idToken)
        // this.checkedIfLoggedIn = true
      } else {
        this.checkedIfLoggedIn = true
      }
    },
    formatRank(rank) {
      if (rank < 60) {
        return 'F'
      } else if (rank < 70) {
        return 'D'
      } else if (rank < 80) {
        return 'C'
      } else if (rank < 90) {
        return 'B'
      } else if (rank < 90) {
        return 'A'
      }
      return 'A+'
    },
    formatCash(cash) {
      if (cash >= 1000000) return `$${(cash/1000000).toFixed(1)}M`
      return `$${(cash/1000).toFixed(1)}K`
    },
    getApiUrl(endpoint) {
      if (process.env.NODE_ENV != 'production') return `http://127.0.0.1:5000/${endpoint}`
      return `https://pulse-backend.onrender.com/${endpoint}`
    },
    getAppUrl(endpoint) {
      if (process.env.NODE_ENV != 'production') return `http://localhost:8080/${endpoint}`
      return `https://trypaper.io/${endpoint}`
    },
    generateDemoTable() {
      // new Grid({
      //   sort: true,
      //   search: true,
      //   columns: ["Name", "Email", "Phone Number"],
      //   data: [
      //     ["John", "john@example.com", "(353) 01 222 3333"],
      //     ["Mark", "mark@gmail.com", "(01) 22 888 4444"],
      //     ["Eoin", "eoin@gmail.com", "0097 22 654 00033"],
      //     ["Sarah", "sarahcdd@gmail.com", "+322 876 1233"],
      //     ["Afshin", "afshin@mail.com", "(353) 22 87 8356"]
      //   ],
        // className: {
        //   td: 'px-6 py-4 whitespace-nowrap text-sm text-gray-900 divide-y divide-gray-200',
        //   th: 'px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider',
        //   table: 'min-w-full divide-gray-200',
        //   tbody: 'bg-white '
        // }
      // }).render(document.getElementById("wrapper"));
    },
    filterFunders() {
      if (this.companyStage === 'bootstrapped') {
        this.filteredFunders = this.funderData.filter(row => row.min_annual_revenue <= 1000000)
      } else if (this.companyStage === 'growth') {
        this.filteredFunders = this.funderData.filter(row => row.min_annual_revenue <= 10000000)
      } else {
        this.filteredFunders = this.funderData
      }
    },
    loginUser(userMetadata, idToken) {
      this.gotFunders = false
      userMetadata.idToken = idToken
      const path = this.getApiUrl('login')
      axios.post(path, userMetadata)
        .then((res) => {
          console.log('did login: ', res.data)
          if (this.$route.query.goto) {
            this.$router.push({ name: this.$route.query.goto, params: { user: userMetadata }})
          } else if (res.data.new || (res.data.user && !res.data.user.hasStripe)) {
            this.$router.push({ name: 'Settings', params: { user: userMetadata }})
          } else {
            this.$router.push({ name: 'Metrics', params: { user: userMetadata }})
          }
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getFunders() {
      this.gotFunders = false
      const path = this.getApiUrl('get_funders')
      let d = {}
      axios.post(path, d)
        .then((res) => {
          console.log('got handle_app_submission: ', res.data)
          this.gotFunders = true
          // this.funderColumns = Object.keys(res.data.columns).filter(c => !['domain', 'data'].includes(c))
          this.funderData = res.data.data
          this.filteredFunders = this.funderData
          // new Grid({
          //   sort: true,
          //   search: true,
            // columns: ["Name", "Email", "Phone Number"],
            // data: res.data.data
            // className: {
            //   td: 'px-6 py-4 whitespace-nowrap text-sm text-gray-900 divide-y divide-gray-200',
            //   th: 'px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider',
            //   table: 'min-w-full divide-gray-200',
            //   tbody: 'bg-white '
            // }
          // }).render(document.getElementById("wrapper"));
        })
        .catch((error) => {
          console.error(error)
        })
    },
    saveFunder(row) {
      row
    },
    applyToFunder(row) {
      let url = `http://${row.domain}/?ref=trypaperio`
      window.open(url, '_blank');
    },
    submitApp() {
      if (!this.appReady) {
        let field = 'email'
        this.appError = `${field} is required.`
        return
      }
      this.submitted = true
      const path = this.getApiUrl('handle_app_submission')
      let d = {application: this.loan, sessionId: ''}
      axios.post(path, d)
        .then((res) => {
          console.log('got handle_app_submission: ', res.data)
        })
        .catch((error) => {
          console.error(error)
        })
    },
    goHome() {
      this.$router.push({ name: 'Landing', params: { userId: 123 }})
    },
    getFunded() {
      this.$router.push({ name: 'Apply', params: { userId: 123 }})
    },
    getRequiredMrr() {
      return ((this.loan.amount / this.loan.multiple) / 1000).toFixed(0)
    },
    setPayoutPeriod(po) {
      this.loan.payoutPeriod = po
      this.updatingPayoutPeriod = false
    },
  },
  computed: {
    appReady() {
      if (this.loan.email.length > 3) return true
      return false
    }
  },
  watch: {
    'companyStage': {
        handler: function () {
          this.filterFunders()
        },
        deep: false
    },
  },
  data() {
      return {
        store: store,
        storeState: store.state,
        checkedIfLoggedIn: false,
        email: '',
        gotFunders: true,
        companyStage: 'bootstrapped',
        funderColumns: ['name', 'paper_rank', 'max_loan_amount', 'min_loan_amount', 'min_annual_revenue'],
        funderCashColumns: ['max_loan_amount', 'min_loan_amount', 'min_annual_revenue'],
        // detailCols: ['']
        columnLabels: {
          name: 'Funder',
          min_loan_amount: 'Revenue'
        },
        funderData: [],
        filteredFunders: [],
        appError: false,
        submitted: false,
        updatingPayoutPeriod: false,
        loan: {
          email: '',
          mrr: 50000,
          amount: 250000,
          rate: .15,
          multiple: 15,
          payoutPeriod: {label: '12 months', months: 12},
          term: 36,
          paybackMonths: 36,
          years: [
            {label: 'Year 1'},
            {label: 'Year 2'},
            {label: 'Year 3'},
            {label: 'Total'},
          ],
          months: [],
          metricCalcType: 'stripe',
          mrrs: [
            {label: 'Current MRR', value: 0},
            {label: '3 months ago', value: 0},
            {label: '6 months ago', value: 0},
            {label: '12 months ago', value: 0},
            {label: '24 months ago', value: 0},
          ]
        },
        payoutPeriods: [
          {label: '12 months', months: 12},
          {label: '18 months', months: 18},
          {label: '24 months', months: 24}
        ],
      }
  }
}
/* eslint-enable no-unused-vars */

</script>

