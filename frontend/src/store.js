// import axios from 'axios';

export const store = {
  state: {
      showDebugStuffNow: false,
      isLoggedIn: false,
      checkedLogin: false,
      gotUserData: false,
      hideSidebar: false,
      user: {
        oauth: false
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
      analysis: {
        uuid: false,
        results: {
          rows: [],
          cols: [],
        },
        viz: {
          type: 'line',
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