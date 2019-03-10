class DeleteMoodEnhancerForm extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    const { user, mood_enhancers, deleteMoodEnhancerBaseUrl } = this.props;
    if (mood_enhancers.length > 1) {
      return (
        <form
          action={`${deleteMoodEnhancerBaseUrl}${user}`}
          method="POST"
          onSubmit={e => e.target.submit()}
        >
          <h4>Delete Mood Enhancers: </h4>
          {mood_enhancers.map(function(enhancer) {
            return (
              <div key={enhancer.mood_enhancer_id}>
                <input
                  type="checkbox"
                  label="check box"
                  name="mood_enhancer"
                  value={enhancer.mood_enhancer_id}
                />
                {enhancer.mood_enhancer}
                <br />
              </div>
            );
          })}
          <br />
          <input type="submit" name="submit" />
        </form>
      );
    } else {
      return (
        <h4>Looks like you don't have any mood enhancers! Add some below!</h4>
      );
    }
  }
}

class UpdateMoodEnhancerForm extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    const { updateBaseUrl } = this.props;
    return (
      <form
        action={updateBaseUrl}
        method="POST"
        onSubmit={e => e.target.submit()}
      >
        <h4>Update Mood Enhancers</h4>
        <input
          type="text"
          name="mood_enhancer_1"
          placeholder="go for a walk.."
        />
        <br />
        <input type="text" name="mood_enhancer_2" placeholder="watch Netlix" />
        <br />
        <input
          type="text"
          name="mood_enhancer_3"
          placeholder="call best friend..."
        />
        <br />
        <input type="submit" name="submit" />
      </form>
    );
  }
}

class Mood_Enhancer extends React.Component {
  constructor() {
    super();
    this.state = {
      user: "",
      mood_enhancers: []
    };
  }

  componentDidMount() {
    let user_id = $("#user_id").text();
    $.get("/update-mood-enhancers/" + user_id, results => {
      this.setState({
        user: results.user,
        mood_enhancers: results.mood_enhancers
      });
    });
  }
  render() {
    const { user, mood_enhancers } = this.state;
    return (
      <div className="App">
        <h1>Update Mood Enhancers</h1>

        <section className="delete-mood-enhancers">
          <DeleteMoodEnhancerForm
            user={user}
            mood_enhancers={mood_enhancers}
            deleteMoodEnhancerBaseUrl="http://localhost:5000/delete-mood-enhancer/"
          />
        </section>

        <hr />

        <section className="update-mood-enhancers">
          <UpdateMoodEnhancerForm updateBaseUrl="http://localhost:5000/mood-enhancers" />
        </section>
      </div>
    );
  }
}

ReactDOM.render(<Mood_Enhancer />, document.getElementById("root"));
