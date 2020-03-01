import AutocompleteJS from 'react-native-autocomplete-input';
import React, { Component } from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';

//TODO: Make this functional
class Autocomplete extends Component {

  constructor(props) {
    super(props);
    this.list = this.props.list;
    this.state = {
      items: [],
      query: '',
      focused: false,
    };
  }

  //TODO: shouldn't set state in componentDidMount()
  componentDidMount() {
    const items = this.props.list;
    this.setState({ items });
  }

  findItem(query) {
    if (query === '') {
      return [];
    }

    const { items } = this.state;
    const regex = new RegExp(`${query.trim()}`, 'i');
    return items.filter(item => item.name.search(regex) >= 0);
  }

  render() {
    const { query } = this.state;
    const items = this.findItem(query);
    const comp = (a, b) => a.toLowerCase().trim() === b.name.toLowerCase().trim();

    return (
      <View containerStyle={styles.container}>
        <AutocompleteJS
          autoCapitalize="none"
          autoCorrect={false}
          listStyle={this.props.listStyle}
          containerStyle={this.props.containerStyle}
          // containerStyle={styles.autocompleteContainer}
          data={items.length === 1 && comp(query, items[0]) ? [] : items}
          defaultValue={query}
          onChangeText={text => {
            console.log('test');
            this.setState({ query: text });
            this.props.onChangeText(query);
          }}
          onFocus={() => this.setState({focused: true})}
          onBlur={() => this.setState({focused: false})}
          placeholder="First Name"
          renderItem={(n, index) => (
            this.state.focused ? 
              <View>
                <TouchableOpacity 
                  id={index} 
                  style={styles.dropdown}
                  onPress={() => {
                    this.setState({ query: n.item.name });
                    this.props.onChangeText(n.item.name);
                  }}>
                  <Text style={styles.itemText}>
                    {n.item.name}
                  </Text>
                </TouchableOpacity>
              </View>
              : <View />
          )}
        />
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#F5FCFF',
    flex: 1,
    paddingTop: 25
  },
  autocompleteContainer: {
    marginLeft: 10,
    marginRight: 10
  },
  dropdown: {
    zIndex: 500,
  },
  itemText: {
    fontSize: 15,
    padding: 10,
    borderWidth: 1,
    borderColor: 'gray',
  },
});

export default Autocomplete;