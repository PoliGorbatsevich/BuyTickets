import React from "react";

class Transaction extends React.Component{
    constructor(props) {
        super(props);
    }
    transaction = this.props.transaction
    datetime = this.props.transaction.datetime
    render() {
        return (
            <div className="performance">
                <h3>Дата и Время: {this.parseTime(this.transaction.datetime)}</h3>
                <h3>description: {this.transaction.description}</h3>
                <h3>payment: {this.transaction.payment}</h3>
                <h3>payment_type: {this.transaction.payment_type}</h3>
                <h3>access: {this.transaction.access}</h3>
            </div>
        )
    }

    parseTime(datetime){
        let str = datetime.slice(0, 10) + " " + datetime.slice(11, 16);
        return str
    }
}

export default Transaction