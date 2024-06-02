import React, { useEffect, useState } from "react";
import './App.css';
import {VotingApi} from './api'

function App() {
  const [paintingsData, setData] = useState([]);

  useEffect(() => {
    VotingApi
      .get()
      .then(data => setData(data['art']))
  }, []);

  return (<div className="App">
    <div>{ paintingsData ? paintingsData.map(
      pd =>
        <Painting key={pd.artist_id} props={pd} />)  :  'Loading...'}</div>
    </div>);
}


class Painting extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      publicUrl: props.props.public_link,
      artistId: props.props.artist_id
    };
  }

  render() {
    return (
      <img
      className="Painting"
      src={this.state.publicUrl}
      alt={"Computer generated abstract art by " + this.state.artistId}
      />
    );
  }
}

export default App;
