import React, { useEffect, useState } from "react";
import './App.css';
import { VotingApi } from './api'
import GoogleButton from './google';

function App() {
  const [ paintingsData, setData ] = useState([]);

  useEffect(() => {
    VotingApi
      .getArt()
      .then(data => setData(data['art']))
  }, []);

  return (
    <div className="App">
    <GoogleButton />
    <div className="container">
    <h2 className="card">Rendered Art</h2>
    </div>

    <div className="container">{ paintingsData ? paintingsData.map(
      pd => <Painting key={pd.artist_id} props={pd} />)  :  'Loading...' }
    </div>
    </div>
  );
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
      <div className="Painting">
      <img
      className="card"
      src={this.state.publicUrl}
      alt={"Computer generated abstract art by " + this.state.artistId}
      onClick={VotingApi.vote}
      />
      </div>
    );
  }
}

export default App;
