import React from "react";
import Performance from "./Performance";

class Performances extends React.Component{
    render() {
        if(this.props.performances.length > 0)
            return (
                <div className="base-block">
                    <h2>Расписание пьес</h2>
                    {this.props.performances.map( el => (
                            <Performance key={el.id} performance={el}
                                     onDelete={this.props.onDelete}
                                     onUpdate={this.props.onUpdate}/>
                    ))}
                </div>
            )
        else
            return (
                <div className="performance">
                    <h3>Пьес нет :(</h3>
                </div>)
    }
}

export default Performances