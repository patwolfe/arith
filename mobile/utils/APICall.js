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
        console.log('204\'d');
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
      token = 'b8a51fad510fae0690a70d07a02f086fdd10f097';
    }

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {...headers, Authorization: `Token ${token}`},
        body: body
      });
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
      token = 'b8a51fad510fae0690a70d07a02f086fdd10f097';
      //return {error: true, message: 'Auth token not found'};
    }

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {...headers, Authorization: `Token ${token}`},
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