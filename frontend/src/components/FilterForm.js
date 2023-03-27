import React from "react";

class FilterForm extends React.Component{
    performance = {}
    constructor(props) {
        super(props);
        this.state = {
        }
    }
    render(){
        return (
            <div className="base-block">
                <h2>Поиск пьес по дате</h2>
                <form ref={(el) => this.MyForm = el}>
                    <input required  type="date" placeholder="Дата"
                           onChange={(e) => {this.setState({date: e.target.value})}}/>
                    <button type="button" onClick={() => {
                        this.performance = {
                            date: this.state.date,
                        }
                        this.props.onFind(this.state.date)
                        this.MyForm.reset()
                        this.setState({date:""})
                    }}>Найти</button>
                    <button type="button" onClick={() =>{
                        this.props.onClear()
                    }}>Очистить</button>
                </form>
            </div>
        )
    }
}

export default FilterForm