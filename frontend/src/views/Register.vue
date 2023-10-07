<template>
    <div class="container">
        <div class="columns">
  <div class="column is-8 is-offset-2">
        
                <h1 class="title"> Register
                </h1>
                <form>
                    <div class="columns">
            <div class="column">
                    
                    <div class="field">
                        <label>Email</label>
                        <div class="control">
                            <input type="email" name="email" class="input"/>
                        </div>
                   
                    </div>
                </div>
                <div class="column">
                    <div class="field">
                        <label>Password</label>
                        <div class="control">
                            <input type="password" name="password" class="input"/>
                        </div>
                    </div>
                </div>
                </div>
                <div class="columns">
            <div class="column">
                    <div class="field">
                        <label>First Name</label>
                        <div class="control">
                            <input type="text" name="first_name" class="input"/>
                        </div>
                    </div>
                </div>
                    <div class="column">
                    <div class="field">
                        <label>Last Name</label>
                        <div class="control">
                            <input type="text" name="last_name" class="input"/>
                        </div>
                    </div>
                </div>
            </div>
                <div class="columns">
            <div class="column">
                    <div class="field">
                        <label>Date of Birth</label>
                        <div class="control">
                            <input type="date" name="dob" class="input"/>
                        </div>
                    </div>
                </div>
              
                    <div class="column">
                      
                      <label>Gender</label>
                      <br/>
                          <div class="select">
  
                              <select>
                                  <option value="m">Male</option>
                                  <option value="f">Female</option>
                                  <option value="o">Other</option>
                              </select>
                          </div>
                       
                      </div>
                
                   
            </div>
           
            <div class="columns">
                <div class="column">
                    <div class="field">
                        <label>Phone</label>
                        <div class="control">
                            <input type="number" name="phone" class="input"/>
                        </div>
                    </div>
                </div>
         
               
          
                    <div class="column">
                    <div class="field">
                        <label>Address</label>
                        <div class="control">
                            <input type="text" name="address" class="input"/>
                        </div>
                    </div>
                </div>

                </div>
                    <div class="field">
                       
                        <div class="control">
                            <button class="button is=success">Submit</button>
                        </div>
                    </div>
                    
                </form>
            </div>
        </div>
    </div>
        
</template>
<script>


export default {
    name:'Register'
}
</script>
