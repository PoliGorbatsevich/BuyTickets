import React from "react";

class Payment extends React.Component{
    user = {}
    constructor(props) {
        super(props);
        this.state = {
            payment: 0
        }
    }
    render(){
        return (
            <div className="base-block">
                <h2>Пополнить баланс</h2>
                <form ref={(el) => this.form = el}>
                    <input placeholder="Сумма"
                           onChange={(e) => {this.setState({payment: e.target.value})}}/>
                    <button type="button" onClick={() => {
                        this.form.reset()
                        if (this.state.payment > 0)
                            this.props.topUpBalance(this.state.payment)
                    }}>Зачислить</button>
                </form>
            </div>
        )
    }
}

export default Payment