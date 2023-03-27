import React from "react";

class PerformanceForm extends React.Component{
    performance = {}
    constructor(props) {
        super(props);
        this.state = {
        }
    }
    render(){
        return (
            <div className="base-block">
                <h2>Форма для добавления пьесы</h2>
                <form ref={(el) => this.MyForm = el}>
                    <input required placeholder="Название пьесы"
                           onChange={(e) => {this.setState({name: e.target.value})}}/>
                    <textarea required placeholder="Описание"
                              onChange={(e) => {this.setState({description: e.target.value})}}/>
                    <input required  type="date" placeholder="Дата"
                           onChange={(e) => {this.setState({date: e.target.value})}}/>
                    <input required type="time" placeholder="Время"
                           onChange={(e) => {this.setState({time: e.target.value})}}/>
                    <input required type="number" placeholder="Количество рядов 1-50" min="1" max="50"
                           onChange={(e) => {this.setState({rowCount: e.target.value})}}/>
                    <input required type="number" placeholder="Длина ряда" min="1" max="50"
                           onChange={(e) => {this.setState({rowLength: e.target.value})}}/>
                    <input required type="number" placeholder="Цена билета" min="1"
                           onChange={(e) => {this.setState({price: e.target.value})}}/>
                    <button type="button" onClick={() => {
                        this.performance = {
                            name: this.state.name,
                            description: this.state.description,
                            date: this.state.date,
                            time: this.state.time,
                        }
                        this.props.onAdd(this.performance,
                            this.state.price,
                            this.state.rowLength,
                            this.state.rowCount)
                        this.MyForm.reset()
                        this.setState({name:"", description:"", date:"", time:"", rowCount:-1, rowLength:-1, price:-1})
                        this.performance = {}
                    }}>Добавить</button>
                </form>
            </div>
        )
    }
}

export default PerformanceForm