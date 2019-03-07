import React, {Component} from "react";
import QrReader from 'react-qr-reader'
import {Link} from "@react-navigation/web";
import {checkin_event} from "../api/API.js"
import {setEvent, setResponse} from "../reducers";
import {connect} from "react-redux";

class Camera extends Component {

    static path = "check/:check";

    static navigationOptions = {
        title: "Camera",
        linkName: "Camera Screen"
    };

    state = {
        result: undefined
    };

    handleScan = data => {
        if (data) {
            this.setState({
                result: data
            });
            this.processRequest(this.props.event.id, {hash: data });

        }
    };

    handleError = err => {
        console.error(err)
    };

    componentWillMount() {
        if (this.props.event === null)
            this.props.navigation.navigate('Intro')
    }

    componentWillUnmount() {
        console.log('Desmontando a câmera')
    }


    render() {
        const { navigation } = this.props;
        const { result } = this.state;

        return (
            <div>
                <p>
                    Posicione o QR code na visão da câmera, abaixo.
                </p>
                <p>
                <button className={'btn btn-outline-info'}
                   onClick={() => this.props.navigation.navigate('Intro')}>Voltar</button>
                </p>

                {
                    result === undefined ?
                        <div className={"row align-items-center"}>
                            <div className={"col"}></div>
                            <div className={"col"}>
                        <div className={""}>
                            <QrReader
                        delay={300}
                        onError={this.handleError}
                        onScan={this.handleScan}
                        style={{width: '100%'}}
                    />
                        </div></div>   <div className={"col"}></div></div> : <h3>Carregando...</h3>
                }


            </div>
        );
    }

    processRequest(event_id, data) {
        const param = this.props.navigation.state.params.check;
        const check = (param === 'in') ? true : (param === 'out' ? false : null);

        if (!this.state.busy) {
            this.setState({busy: true});
            checkin_event(event_id, data, check).then(response => {
                this.setState({cpf: ''});
                this.props.setResponse({check: check, ...response.data});
                this.props.navigation.navigate('Message');
            }).catch(error => {
                if (error.response) {
                    this.props.setResponse({check: check, ...error.response.data});
                    this.props.navigation.navigate('Message');
                } else if (error.request) {
                    // The request was made but no response was received
                    // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
                    // http.ClientRequest in node.js
                    console.log(error.request);
                } else {
                    // Something happened in setting up the request that triggered an Error
                    console.log('Error', error.message);
                }
                console.log(error.config);
            }).finally(() => {
                this.setState({busy: false});
            });
        }
    }
}


const mapStateToProps = state => {
    return { event: state.event };
};

function mapDispatchToProps(dispatch) {
    return {
        setResponse: event_id => dispatch(setResponse(event_id))
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(Camera)