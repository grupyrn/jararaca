import React, {Component} from "react";
import {setResponse} from "../reducers";
import {connect} from "react-redux";
import config from "../config"
import {CSSTransitionGroup} from 'react-transition-group'
import Alert from "./Intro";
import Animation from "./utils/Animation"; // ES6

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
        let {status, message, attendee, check, typeStatus} = data;
        console.log(data);

        if (status.includes('_OK'))
            typeStatus = 'success';
        else if (status.startsWith('EVENT'))
            typeStatus = 'danger';

        return <Alert type={typeStatus}><h5>{message}</h5></Alert>
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
                <Animation>
                    {this.renderResponse()}
                </Animation>
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