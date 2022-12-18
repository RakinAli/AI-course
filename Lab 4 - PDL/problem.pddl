(define (problem festival) ; the problem name
(:domain tavern) ; the domain in which the problem takes place
(:objects ; the objects in the problem
    ; reserved parties
    livingstone
    the_fellowship
    mardi_gras
    friends
    vox_machina
    ; drop in parties
    p1
    p2
    p3
    p4
    ; rooms
    suite
    cellar
    regular
    deluxe
    ; sizes
    small
    medium
    large
    ;
    thursday
    friday
    saturday
    sunday
)
(:init ; the initial world state
    ; the parties
    (party livingstone) (party the_fellowship) (party mardi_gras) (party vox_machina) (party friends)
    (party p1) (party p2) (party p3) (party p4)
    ; the rooms
    (room suite) (room deluxe) (room cellar) (room regular)
    ; the sizes
    (size small) (size large) (size medium)
    ; the days
    (day thursday) (day friday) (day saturday) (day sunday)
    ; the reservations
        ;Living Stone
    (has_reservation livingstone suite thursday)(has_reservation livingstone suite friday) (has_reservation livingstone suite saturday)
        ; The Fellowship
    (has_reservation the_fellowship deluxe saturday)
        ; Mardi Gras
    (has_reservation mardi_gras cellar friday) (has_reservation mardi_gras cellar saturday)
        ; Vox Machina
    (has_reservation vox_machina deluxe friday)
        ; friends
    (has_reservation friends regular saturday)

    ;TODO the drop in party sizes
    (is_size p1 small) (is_size p2 medium) (is_size p3 medium) (is_size p4 large)

    ; the room sizes
    (is_size suite small) 
    (is_size cellar medium)
    (is_size regular medium)
    (is_size deluxe large)

    ; the size structure :
    (fits small small) 
    (fits small medium) (fits medium medium) 
    (fits small large)(fits medium large) (fits large large)
     

    ; thursday is the current day
    (is_current_day thursday)

    ; the day order
    (is_next_day thursday friday) (is_next_day friday saturday)(is_next_day saturday sunday)
    
    ; the rooms are empty and clean
    (is_vacant suite) (is_clean suite) 
    (is_vacant deluxe) (is_clean deluxe)
    (is_vacant cellar) (is_clean cellar)
    (is_vacant regular) (is_clean regular)

)
;TODO
(:goal ; the end goals
    ; all rooms are booked each day
    ; the parties with reservations were booked accordingly
    ;Your goal is that all parties with reservations are booked for their corresponding day.
    ;And that all of the four rooms are booked for all of the four days
        (and
        ; Thursday, all rooms are booked AND all parties with reservations are booked
        (has_booked_room suite thursday) (has_booked_room cellar thursday) (has_booked_room regular thursday) (has_booked_room deluxe thursday)
        
        ; Friday, all rooms are booked AND all parties with reservations are booked
        (has_booked_room suite friday) (has_booked_room cellar friday)(has_booked_room regular friday) (has_booked_room deluxe friday) 

        ; Saturday, all rooms are booked AND all parties with reservations are booked
        (has_booked_room suite saturday) (has_booked_room cellar saturday)(has_booked_room regular saturday) (has_booked_room deluxe saturday)

        ; Sunday, all rooms are booked AND all parties with reservations are booked
        (has_booked_room suite sunday) (has_booked_room cellar sunday)(has_booked_room regular sunday) (has_booked_room deluxe sunday)

        ; Living Stone   
        (has_booked_party livingstone thursday) (has_booked_party livingstone friday) (has_booked_party livingstone saturday)

        ; Mardi Gras
        (has_booked_party mardi_gras friday) (has_booked_party mardi_gras saturday)

        ; Vox Machina
        (has_booked_party vox_machina friday)

        ; friends
        (has_booked_party friends saturday)

        ; the_fellowship
        (has_booked_party the_fellowship saturday)

        ; Drop in parties thursday
        (has_booked_party p2 thursday) (has_booked_party p3 thursday) (has_booked_party p4 thursday)

        ; Drop in parties friday
        (has_booked_party p3 friday) 

        ; Drop in parties saturday

        ; Drop in parties sunday
        (has_booked_party p1 sunday) (has_booked_party p2 sunday) (has_booked_party p3 sunday) (has_booked_party p4 sunday)
    )
)
)
