// import React, { useContext } from 'react'
// import './FoodDisplay.css'
// import { StoreContext } from '../../context/StoreContext'
// import FoodItem from '../FoodItem/FoodItem.jsx'

// const FoodDisplay = ({category}) => {

//     const {food_list} = useContext(StoreContext)

//   return (
//     <div className='food-display' id='food-display'>
//         <h2 className='h2we'>Top dishes near you</h2>
//         <div className="food-display-list">
//             {food_list.map((item,index)=>{
//               if(category==="All" || category===item.category){
//                 return <FoodItem key={index} id={item._id} name={item.name} description={item.description} price={item.price} image={item.image} />
//               }      
//             })}
//         </div>
//     </div>
//   )
// }

// export default FoodDisplay



import React, { useContext } from 'react';
import './FoodDisplay.css';
import { StoreContext } from '../../context/StoreContext';
import FoodItem from '../FoodItem/FoodItem';

const FoodDisplay = ({ category }) => {
  const { food_list } = useContext(StoreContext); // Accessing food_list from context

  return (
    <div className='food-display' id='food-display'>
      <h2 className='h2we'>Top dishes near you</h2>
      <div className="food-display-list">
        {food_list && food_list.length > 0 ? (
          food_list.map((item, index) => {
            if (category === "All" || category === item.category) {
              return (
                <FoodItem
                  key={index}
                  id={item._id}
                  name={item.name}
                  description={item.description}
                  price={item.price}
                  image={item.image}
                />
              );
            }
            return null; // Return null for items that don't match the category
          })
        ) : (
          <p>No dishes available</p> // Display message if food_list is empty
        )}
      </div>
    </div>
  );
};

export default FoodDisplay;
