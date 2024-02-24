import "./Card.css"

const Card = ({imgSource, title, onClick}) => {
  return (
    <div className="card" onClick={onClick}>
        <img src={imgSource}/>
        <p>{title}</p>
    </div>
  )
}

export default Card