import "./Button.css"

const Button = ({name, onClick}) => {
  return (
    <>
        <button type="submit" className="form-button" onClick={onClick}>{name}
        </button>
    </>
  )
}

export default Button