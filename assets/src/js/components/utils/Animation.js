import React from "react";
import {CSSTransitionGroup} from "react-transition-group";

const Animation = (props) => {
    return <CSSTransitionGroup
        transitionName="example"
        transitionAppear={true}
        transitionAppearTimeout={400}
        transitionEnterTimeout={400}
        transitionLeaveTimeout={400}
        transitionEnter={true}
        transitionLeave={false}>
            {props.children}
    </CSSTransitionGroup>;
};


export default Animation;