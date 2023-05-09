import React, { useState, useEffect } from 'react';

function AddListingPopup({ onClose, onSubmit }) {
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [description, setDescription] = useState('');
  const [condition, setCondition] = useState('');
  const [date, setDate] = useState(formatDate(addMinutes(new Date(), 0, 1)));
  const [image, setImage] = useState(null);
  const [addListEnable, setAddListEnable] = useState(true);
  const [errors, setErrors] = useState("");

  useEffect(() => {
    if (name.trim() !== '' && price.trim() !== '' && description.trim() !== '' && condition.trim() !== '' && date.trim() !== '' && image !== null) {
      setAddListEnable(false);
    } else {
      setAddListEnable(true);
    }
  }, [name, price, description, condition, date, image]);

  const handleNameChange = (event) => {
    setName(event.target.value);
  };

  const handlePriceChange = (event) => {
    setPrice(event.target.value);
  };

  const handleDescriptionChange = (event) => {
    setDescription(event.target.value);
  };

  const handleConditionChange = (event) => {
    setCondition(event.target.value);
  };

  const handleImageChange = (event) => {
    setImage(event.target.files[0]);
  };

  const handleDateChange = (event) => {
    setDate(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);

    let date_obj = new Date(date)
    let utcdate = date_obj.toISOString()
    formData.set('date', utcdate)

    fetch('/add-item', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 1) {
          setErrors("");
          onSubmit()
          onClose()
          window.location.reload();
        } else {
          setErrors(data.field);
        }
      })
      .catch(error => console.error(error));
  };

  return (
    <div className="add-listing-popup">
      <h2>Add Listing</h2>
      <form onSubmit={handleSubmit}>
        {errors !== "" && <div className="error-message">{errors}</div>}
        <div className="form-field">
          <br />
          <label>Item Name:</label>
          <input name="Item_Name" type="text" value={name} onChange={handleNameChange} />
        </div>
        <div className="form-field">
          <label>Base Price:</label>
          <input name="Item_Price" type="number" value={price} onChange={handlePriceChange} />
        </div>
        <div className="form-field">
          <label>Description:</label>
          <textarea name="Item_Desc" value={description} onChange={handleDescriptionChange} />
        </div>
        <div className="form-field">
          <label>Condition:</label>
          <select name="condition" value={condition} onChange={handleConditionChange}>
            <option value="" disabled hidden>--- Select From Below ---</option>
            <option name="condition" value="Brand New">Brand New</option>
            <option name="condition" value="Like New">Like New</option>
            <option name="condition" value="Good">Good</option>
            <option name="condition" value="Fair">Fair</option>
            <option name="condition" value="Poor">Poor</option>
          </select>
        </div>
        <div className="form-field">
          <label>Auction End Date:</label>
          <input id="Date" min={formatDate(new Date())} name="date" value={date} type="datetime-local" onChange={handleDateChange} />
        </div>
        <div className="form-field">
          <label>Image:</label>
          <input name="image" type="file" onChange={handleImageChange} />
        </div>
        <button type="submit" disabled={addListEnable}>Add Listing</button>
        <button type="button" onClick={onClose}>Cancel</button>
      </form>
    </div>
  );
}

function addMinutes(date, minutes, hours) {
    return new Date(date.getTime() + minutes*60000 + hours*60000*60);
}

function formatDate(date){
  let dd = date.getDate()
  let mo = date.getMonth() + 1; //January is 0
  let yyyy = date.getFullYear();
  let hh = date.getHours()
  let mn = date.getMinutes()
  if (dd < 10) {
    dd = '0' + dd;
  }
  if (mo < 10) {
    mo = '0' + mo;
  }
  if (hh < 10) {
    hh = '0' + hh;
  }
  if (mn < 10) {
    mn = '0' + mn;
  }
  return yyyy + '-' + mo + '-' + dd + 'T' + hh + ':' + mn
}

export default AddListingPopup;