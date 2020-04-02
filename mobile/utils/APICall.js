import { AsyncStorage } from 'react-native';

export default {
  async PostNoAuth(url, headers, body) {
    try {
      const response = await fetch(url, {
        method: 'POST', 
        headers: headers,
        body: body,
      });
      
      if (response.status === 204) {
        return {error: false, ok: response.ok};
      }
      
      let res = await response.json();
      return {error: false, ok: response.ok, res: res};
    }
    catch (e) {
      console.log(e);
      return {error: true};
    }
  },

  async PostAuth(url, headers, body) {
    let token = await AsyncStorage.getItem('token');
    if (token === null) {
      console.log('token is null in async storage');
      return {error: true, message: 'No auth token'};
    }
  
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {...headers, Authorization: `Bearer ${token}`},
        body: body
      });
     
      if (response.status === 204) {
        return {error: false, ok: response.ok};
      }
     
      let res = await response.json();
      return {error: false, ok: response.ok, res: res};
    }

    catch (e) {
      console.log(e);
      return {error: true, message: 'Network error'};
    }
  },

  async GetAuth(url, headers) {
    let token = await AsyncStorage.getItem('token');
    if (token === null) {
      console.log('token is null in async storage');
      return {error: true, message: 'No auth token'};
    }

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {...headers, Authorization: `Bearer ${token}`},
      });
      let res = await response.json();
      return {error: false, ok: response.ok, res: res};
    }

    catch (e) {
      console.log(e);
      return {error: true, message: 'Network error'};
    }
  },

  async storeToken(token) {
    try {
      await AsyncStorage.setItem('token', token);
      return true;
    }
    catch (e) {
      console.log(e);
      return false;
    }
  }
};
