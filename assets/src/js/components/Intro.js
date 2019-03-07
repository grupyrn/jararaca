import React, {Component} from "react";
import {current_events} from "../api/API";
import {connect} from "react-redux";
import {setEvent} from "../reducers/index";


class Intro extends Component {
    static path = "check";

    static navigationOptions = {
        title: "Intro",
        linkName: "Intro Screen"
    };

    constructor(props) {
        super(props);
        this.state = {
            event: null,
            busy: true,
            error: null,
            data: null
        }
    }


    componentDidMount() {
        if (this.state.busy) {
            current_events().then(response => {
                console.log('data', response);
                this.setState({busy: false, data: response.data});
                if (response.data.length === 1) {
                    this.selectEvent(response.data[0]);
                }
            }).catch(error => {
                if (error.response) {
                    console.log(error.response);
                    this.setState({error: 'Falha ao conectar: '+error.response.statusText})
                } else if (error.request) {
                    // The request was made but no response was received
                    // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                    // http.ClientRequest in node.js
                    console.log(error.request);
                    this.setState({error: 'Erro: o servidor não respondeu apropriadamente.'});
                } else {
                    // Something happened in setting up the request that triggered an Error
                    this.setState({error: 'Requisição inválida.'});
                    console.log('Error', error.message);
                }
                console.log(error.config);
            }).finally(() => {
                this.setState({busy: false});
            });
        }
    }

    selectEvent(event) {
        const {setEvent} = this.props;
        setEvent(event);
    }

    renderItems() {
        const lista = [];
        this.state.data.forEach((event, i) => {
            lista.push(<div key={event.id}>
                <button className={"btn btn-secondary"} onClick={() => this.selectEvent.bind(this)(event)}>{event.name}</button><br />
            </div>)
        });

        // console.log(this.state.data);
        return lista;
    }

    render() {
        return (
            <div>
                {
                    this.state.busy ?
                        <p>Carregando...</p> :
                        this.state.error ? <div className="alert alert-danger" role="alert">
                            {this.state.error}</div> :
                            this.props.event == null ?
                                <div>
                                    <p>Selecione o evento: </p>

                                    <div className={'lista'}>
                                        <div>
                                            {this.renderItems()}
                                        </div>
                                    </div>
                                </div>
                                :
                                <div>
                                    <h4>Bem vindo(a) ao {this.props.event.name} </h4>
                                    {/*<Link routeName="Camera" className={'btn btn-primary'} params={{ check: 'in' }}>Realizar Check-in</Link> <br />*/}
                                    <p>
                                        <button className={'btn btn-outline-success btn-lg'}
                                           onClick={() => this.props.navigation.navigate('Camera', {check: 'in'})}>Realizar
                                            Check-in</button>
                                    </p><p>
                                    <button className={'btn btn-outline-danger btn-lg'}
                                       onClick={() => this.props.navigation.navigate('Camera', {check: 'out'})}>Realizar
                                        Check-out</button>
                                </p>
                                </div>
                }
            </div>

        );
    }

}

const mapStateToProps = state => {
    return {event: state.event};
};

function mapDispatchToProps(dispatch) {
    return {
        setEvent: event_id => dispatch(setEvent(event_id))
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(Intro)