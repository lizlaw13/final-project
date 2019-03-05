class App extends React.Component {
  constructor() {
    super();
    this.state = {
      moods: [],
      activities: [],
      note: [],
      entry: {},
      entry_activities: [],
      entry_id: ""
    };
  }

  componentDidMount() {
    let entry_id = $("#entry_id").text();
    console.log(entry_id);
    $.get("/update/" + entry_id, results => {
      console.log(results);
      this.setState({
        entry_id: entry_id,
        moods: results.moods,
        activities: results.activities,
        entry: results.entry,
        entry_activities: results.entry_activities
      });
    });
  }

  render_no_activities() {
    if (this.state.entry_activities.length === 0) {
      return "Looks like you don't have any activities....";
    }
  }

  render_no_note() {
    if (this.state.entry.entry_description == null) {
      return "Looks like you do not have a note for this entry...";
    }
  }
  onActivity(event) {
    event.preventDefault();
    console.log(this.refs.check_me.value);
    this.setState({ activity_id: this.refs.check_me.value });
  }

  render() {
    const entry = this.state.entry;
    return (
      <div className="App">
        <h1>Update Your Entry</h1>
        <div key={entry.entry_mood}>
          <strong>
            <p>
              Your mood for {entry.entry_date} was {entry.entry_mood}!
            </p>
          </strong>
        </div>
        <h4>{this.render_no_activities()}</h4>
        <div>
          {this.state.entry_activities.length >= 1 && (
            <div>
              {" "}
              {this.state.entry_activities.map(function(entry_activitiy) {
                return (
                  <div key={entry_activitiy.activity_id}>
                    <li>{entry_activitiy.activity}</li>
                  </div>
                );
              })}
            </div>
          )}
        </div>
        <div>
          {entry.entry_description !== null && (
            <div>
              {" "}
              <div key={entry.entry_description}>
                <p>
                  <strong>Note: </strong>
                  {entry.entry_description}
                </p>
              </div>
            </div>
          )}
        </div>
        <div>
          {entry.entry_description && (
            <div>
              {" "}
              <form
                action={`http://localhost:5000/delete-note-entry/${
                  entry.entry_id
                }`}
                method="POST"
                onSubmit={e => e.target.submit()}
              >
                <h4>Delete Note: </h4>
                <div key={entry.entry_id}>
                  {entry.entry_description} <br /> <br />
                  <input
                    type="submit"
                    name="Delete"
                    value="Delete"
                    onSubmit={e => onActivity()}
                  />
                  <br />
                </div>
              </form>
            </div>
          )}
        </div>
        <div>
          {this.state.entry_activities.length >= 1 && (
            <div>
              {" "}
              <form>
                <h4>Delete Activity/ Activities: </h4>
                {this.state.entry_activities.map(function(entry_activitiy) {
                  return (
                    <div key={entry_activitiy.activity_id}>
                      <input
                        ref="check_me"
                        type="checkbox"
                        name="activity_category"
                        value={entry_activitiy.activity_id}
                      />
                      {entry_activitiy.activity}
                      <br />
                    </div>
                  );
                })}
                <br />
                <input
                  type="submit"
                  name="submit"
                  onClick={this.onActivity.bind(this)}
                />
              </form>
            </div>
          )}
        </div>
        <hr />
        <form method="POST">
          Select a mood:
          <br />
          <br />
          {this.state.moods.map(function(mood) {
            return (
              <div key={mood.mood_id}>
                <input type="radio" name="mood" value={mood.mood_id} />
                {mood.verbose_mood}
                <br />
              </div>
            );
          })}
          <br />
          <br />
          Select activities:
          <br />
          <br />
          {this.state.activities.map(function(activity) {
            return (
              <div key={activity.activity_category_id}>
                <input
                  type="radio"
                  name="activity_category"
                  value={activity.activity_category_id}
                />
                {activity.verbose_category}
                <br />
              </div>
            );
          })}
          <br />
          <br />
          Optional Note:
          <br />
          <br />
          <input
            type="text"
            name="description"
            placeholder="2 hour exercise class, drinks with friends"
            size="40"
          />
          <br />
          <br />
          <input type="submit" name="submit" />
        </form>
      </div>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("root"));
