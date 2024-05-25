class ContactForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = { name: '', email: '' };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;

        this.setState({
            [name]: value
        });
    }

    handleSubmit(event) {
        alert('name: ' + this.state.name + ', email: ' + this.state.email);
        event.preventDefault();
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <label>
                    name:
                    <input type="text" name="name" value={this.state.name} onChange={this.handleChange} />
                </label>
                <label>
                    email:
                    <input type="email" name="email" value={this.state.email} onChange={this.handleChange} />
                </label>
                <button type="submit">submit</button>
            </form>
        );
    }
}

ReactDOM.render(<ContactForm />, document.getElementById('root'));