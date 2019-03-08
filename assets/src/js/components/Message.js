import React, {Component} from "react";
import {setResponse} from "../reducers";
import {connect} from "react-redux";

class Message extends Component {

    static path = "check/message";

    componentDidMount() {
        setTimeout(() => {
            this.props.navigation.navigate('Intro');
        }, 3500);
    }

    renderResponse() {
        const {status, message, attendee, check} = this.props.response;

        if (status === 'OK') {
            if (check){
                return (
                    <div className="alert alert-success" role="alert">
                        <h5>Bem vindo(a), {attendee.name}!</h5></div>
                )
            }
            return (
                <div className="alert alert-success" role="alert">
                    <h5>Até mais, {attendee.name}!</h5></div>
            )
        } else {
            return <div className="alert alert-warning" role="alert">
                <h5>{message}</h5></div>
        }
    }

    componentWillMount() {
        if (this.props.event === null)
            this.props.navigation.navigate('Intro')
    }

    componentWillUnmount() {
        this.props.setResponse(null);
    }

    render() {
        return (
            <div>
                {this.renderResponse()}
            </div>
        );
    }

}


const mapStateToProps = state => {
    return {
        event: state.event, response: state.response
    };
};

function mapDispatchToProps(dispatch) {
    return {
        setResponse: event_id => dispatch(setResponse(event_id))
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(Message)