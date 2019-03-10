import React, {Component} from "react";
import {setResponse} from "../reducers";
import {connect} from "react-redux";
import config from "../config"
import {CSSTransitionGroup} from 'react-transition-group' // ES6

class Message extends Component {

    static path = "check/message";

    static navigationOptions = {
        title: config.window_title,
    };


    componentDidMount() {
        setTimeout(() => {
            this.props.navigation.navigate('Intro');
        }, 3500);
    }

    renderResponse() {
        const data = {typeStatus: 'warning', ...this.props.response};
        const {status, message, attendee, check, typeStatus} = data;
        console.log(data);

        if (status === 'OK') {
            if (check) {
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
            return <div className={"alert alert-"+ typeStatus} role="alert">
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
                <CSSTransitionGroup
                    transitionName="example"
                    transitionAppear={true}
                    transitionAppearTimeout={400}
                    transitionEnterTimeout={400}
                    transitionLeaveTimeout={400}
                    transitionEnter={true}
                    transitionLeave={true}>
                    {this.renderResponse()}
                </CSSTransitionGroup>
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