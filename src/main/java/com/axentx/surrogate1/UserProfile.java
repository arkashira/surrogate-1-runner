
package com.axentx.surrogate1;

import javax.persistence.*;
import java.util.Date;

@Entity
public class UserProfile {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String username;
    private String password;
    private String firstName;
    private String lastName;
    private Date createdAt;
    private Date updatedAt;

    // getters and setters
}