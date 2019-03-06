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
          <h4>Delete Note: </h4>
          <p>{entry.entry_description}</p>
          <input type="submit" name="Delete" value="Delete" />
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
    if (entry_activities) {
      return (
        <form
          action={`${deleteActivityBaseUrl}${entry.entry_id}`}
          method="POST"
          onSubmit={e => e.target.submit()}
        >
          <h4>Delete Activity/ Activities: </h4>
          {entry_activities.map(function(entry_activitiy) {
            return (
              <div key={entry_activitiy.activity_id}>
                <input
                  type="checkbox"
                  label="check box"
                  name="activity_category"
                  value={entry_activitiy.activity_id}
                />
                {entry_activitiy.activity}
                <br />
              </div>
            );
          })}
          <br />
          <input type="submit" name="submit" />
        </form>
      );
    }
    return null;
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
        action={`${updateEntryBaseUrl}${entry.user_id}`}
        method="POST"
        onSubmit={e => e.target.submit()}
      >
        Select a mood:
        <br />
        <br />
        {moods.map(function(mood) {
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
        {activities.map(function(activity) {
          return (
            <div key={activity.activity_category_id}>
              <input
                type="checkbox"
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
    let activities = <h4>Looks like you don't have any activities...</h4>;
    let description = <h4>Looks like you don't have a note...</h4>;

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
      description = (
        <p>
          <strong>Note: </strong>
          {entry.entry_description}
        </p>
      );
    }

    return (
      <div className="App">
        <h1>Update Your Entry</h1>
        <section className="moods" key={entry.entry_mood}>
          <strong>
            <p>
              Your mood for {entry.entry_date} was {entry.entry_mood}!
            </p>
          </strong>
        </section>

        <section className="activities">{activities}</section>

        <section className="description">{description}</section>

        <section className="delete-description">
          <DeleteNoteForm
            entry={entry}
            deleteNoteBaseUrl="http://localhost:5000/delete-note-entry/"
          />
        </section>

        <section className="delete-description">
          <DeleteActivityForm
            entry_activities={entry_activities}
            deleteActivityBaseUrl="http://localhost:5000/modified-entry/"
            entry={entry}
          />
        </section>

        <hr />
        <section className="update-entry">
          <UpdateEntryForm
            entry={entry}
            moods={this.state.moods}
            activities={this.state.activities}
            updateEntryBaseUrl="http://localhost:5000/updated-entry/"
          />
        </section>

        <hr />
        <br />
        <a href={`/user/${entry.user_id}`}>Homepage</a>
      </div>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("root"));
