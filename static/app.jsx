class DeleteNoteForm extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    const { entry, deleteNoteBaseUrl } = this.props;
    if (entry.entry_description) {
      return (
        <form
          action={`${deleteNoteBaseUrl}${entry.entry_id}`}
          method="POST"
          onSubmit={e => e.target.submit()}
        >
          <h4 className="title">Delete Note</h4>
          <p>{entry.entry_description}</p>
          <button
            type="submit"
            name="Delete"
            className="delete-note-button round-button"
          >
            Delete
          </button>
        </form>
      );
    }
    return null;
  }
}

class DeleteActivityForm extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    const { entry_activities, deleteActivityBaseUrl, entry } = this.props;
    console.log(entry_activities.length);
    if (entry_activities.length > 0) {
      return (
        <form
          action={`${deleteActivityBaseUrl}${entry.entry_id}`}
          method="POST"
          onSubmit={e => e.target.submit()}
        >
          <h4 className="title">Delete Activity/ Activities </h4>
          {entry_activities.map(function(entry_activitiy) {
            return (
              <div key={entry_activitiy.activity_id}>
                <div className="form-check">
                  <input
                    className="form-check-input"
                    type="checkbox"
                    name="activity_category"
                    value={entry_activitiy.activity_id}
                  />
                  {entry_activitiy.activity}
                </div>
              </div>
            );
          })}
          <br />
          <button
            type="submit"
            name="Delete"
            className="delete-activity-button round-button"
          >
            Delete
          </button>
        </form>
      );
    } else {
      return <p>Looks like you don't have any activities. Add some below!</p>;
    }
  }
}

class UpdateEntryForm extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    const { entry, moods, activities, updateEntryBaseUrl } = this.props;
    return (
      <form
        action={`${updateEntryBaseUrl}${entry.entry_id}`}
        method="POST"
        onSubmit={e => e.target.submit()}
        className="add-entry-form"
      >
        <h4 className="title">Update Your Entry </h4>
        <p className="label">Select a mood</p>
        {moods.map(function(mood) {
          return (
            <div key={mood.mood_id} className="form-check">
              <input
                type="radio"
                name="mood"
                value={mood.mood_id}
                className="form-check-input"
              />
              {mood.verbose_mood}
            </div>
          );
        })}
        <p className="label">Select activity category</p>
        {activities.map(function(activity) {
          return (
            <div key={activity.activity_category_id} className="form-check">
              <input
                type="checkbox"
                name="activity_category"
                value={activity.activity_category_id}
                className="form-check-input"
              />
              {activity.verbose_category}
            </div>
          );
        })}
        <br />
        <div className="form-group">
          <label className="label">Optional Note:</label>
          <input
            type="text"
            className="form-control"
            id="formGroupExampleInput"
            placeholder="Ex. 2 hour exercise class, drinks with friends"
            name="description"
            size="40"
          />
        </div>
        <button
          className="entry-submit"
          type="submit"
          name="submit"
          id="entry-submit"
        >
          Submit
        </button>
      </form>
    );
  }
}

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

    $.get("/update/" + entry_id, results => {
      this.setState({
        entry_id: entry_id,
        moods: results.moods,
        activities: results.activities,
        entry: results.entry,
        entry_activities: results.entry_activities
      });
      console.log(this.state.entry_activities);
    });
  }
  render() {
    const { entry, entry_activities } = this.state;
    let activities;
    let description = <h6>Looks like you don't have a note...</h6>;

    if (entry_activities.length > 0) {
      let entry_activities_lis = entry_activities.map(entry_activity => {
        return (
          <li key={entry_activity.activity_id}>{entry_activity.activity}</li>
        );
      });
      // Reassign activities if there are activities in the list
      activities = (
        <ul className="entry-activities-list">{entry_activities_lis}</ul>
      );
    }

    if (entry.entry_description) {
      description = <p>{entry.entry_description}</p>;
    }

    return (
      <div className="App container">
        <div className="row">
          <div className="col left-container">
            <div className="card current-entry-card">
              <div className="text-container">
                <h4 className="title">Current Entry </h4>
                <section className="moods" key={entry.entry_mood}>
                  <p className="date">{entry.entry_date}</p>
                  <p className="mood">Mood</p>
                  <p>{entry.entry_mood}</p>
                </section>
                <section>
                  <p className="activities">Activity/Activities</p>
                  {activities}
                </section>
                <section>
                  <p className="note">Note</p>
                  {description}
                </section>
              </div>
            </div>
            <div className="card current-delete-form">
              <section className="delete-description">
                <DeleteNoteForm
                  entry={entry}
                  deleteNoteBaseUrl="http://localhost:5000/delete-note-entry/"
                />
              </section>
              <section className="delete-activitiy">
                <DeleteActivityForm
                  entry_activities={entry_activities}
                  deleteActivityBaseUrl="http://localhost:5000/modified-entry/"
                  entry={entry}
                />
              </section>
            </div>
          </div>
          <div className="col">
            <div className="card">
              <section className="update-entry">
                <UpdateEntryForm
                  entry={entry}
                  moods={this.state.moods}
                  activities={this.state.activities}
                  updateEntryBaseUrl="http://localhost:5000/updated-entry/"
                />
              </section>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("root"));
