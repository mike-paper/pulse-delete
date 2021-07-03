// import axios from 'axios';

export const store = {
  state: {
      showDebugStuffNow: false,
      isLoggedIn: false,
      checkedLogin: false,
      gotUserData: false,
      gotDbt: false,
      hideSidebar: false,
      user: {
        oauth: false,
        hasStripe: false
      },
      settings: {
        notifications: {
          weekly: {
            slack: false,
            email: true,
          },
          monthly: {
            slack: true,
            email: true,
          },
        }
      },
      dbt: {},
      jobStatuses: {},
      analysis: {
        uuid: false,
        results: {
          rows: [],
          cols: [],
        },
        viz: {
          type: 'grid',
          encoding: {
            "x": {"field": false, "type": "ordinal"},
            "y": {"field": false, "type": "quantitative"},
          }
        }
      },
      userData: {
        savedFunders: []
      },
      msg: {
        show: false,
        primary: '',
        secondary: '',
        icon: '',
        type: '',
        time: 8000,
      }
  }
}