
 **Model Inheritance** 
 
Django supports model inheritance. It works in a similar way to standard class inheritance in Python. Django offers the following three options to use model inheritance: 

• ***Abstract models:*** 

An abstract model is a base class in which you define fields you want to include in all child models. Django doesn't create any database tables for abstract models. A database table is created for each child model, including the fields inherited from the abstract class and the ones defined in the child model. To mark a model as abstract, you need to include abstract=True in its Meta class. Django will recognize that it is an abstract model and will not create a database table for it.
Useful when you want to put some common information into several models.

 • ***Multi-table model inheritance:*** 
 
 In multi-table inheritance, each model corresponds to a database table. Django creates a OneToOneField field for the relationship between the child model and its parent model. To use multi-table inheritance, you have to subclass an existing model. Django will create a database table for both the original model and the sub-model.Applicable when each model in the hierarchy is considered a complete model by itself. 
 
 • ***Proxy models:***
 
 A proxy model changes the behavior of a model. Both models operate on the database table of the original model. To create a proxy model, add proxy=True to the Meta class of the model. Useful when you need to change the behavior of a model, for example, by including additional methods, changing the default manager, or using different meta options.
 
 
**Formsets for Category modules** 

 Django comes with an abstraction layer to work with multiple forms on the same page. Formsets manage multiple instances of a certain Form or ModelForm. All forms are submitted at once and the formset takes care of the initial number of forms to display, limiting the maximum number of forms that can be submitted and validating all the forms.
 
***Contenttypes Framework***

Django includes a contenttypes framework located at django.contrib. contenttypes. The django.contrib.contenttypes application is included in the INSTALLED_APPS setting by default when you create a new project using the startproject command. It is used by other contrib packages, such as the authentication framework and the administration application. The contenttypes application contains a ContentType model. Instances of this model represent the actual models of your application, and new instances of ContentType are automatically created when new models are installed in your project. The ContentType model has the following fields: 

• app_label: This indicates the name of the application that the model belongs to. This is automatically taken from the app_label attribute of the model Meta options. For example, your Image model belongs to the images application.

 • model: The name of the model class. 
 
 • name: This indicates the human-readable name of the model. This is automatically taken from the verbose_name attribute of the model Meta options.
 In generic relations, ContentType objects play the role of pointing to the model used for the relationship. You will need three fields to set up a generic relation in a model: 
 
 • A ForeignKey field to ContentType: This will tell you the model for the relationship .
 
 • A field to store the primary key of the related object: This will usually be a PositiveIntegerField to match Django's automatic primary key fields .• A field to define and manage the generic relation using the two previous fields: The contenttypes framework offers a  GenericForeignKey field for this purpose.
 
Django does not create any field in the database for GenericForeignKey fields.

Django offers a QuerySet method called `select_related()` that allows you to retrieve related objects for one-to-many relationships. This translates to a single, more complex QuerySet, but you avoid additional queries when accessing the related objects. The select_related method is for ForeignKey and OneToOne fields. It works by performing a SQL JOIN and including the fields of the related object in the SELECT statement.

`select_related()` will help you to boost performance for retrieving related objects in one-to-many relationships. However, `select_related()` doesn't work for many-to-many or many-to-one relationships (ManyToMany or reverse ForeignKey fields). Django offers a different QuerySet method called `prefetch_related` that works for many-to-many and many-to-one relationships in addition to the relationships supported by select_related(). The `prefetch_related()` method performs a separate lookup for each relationship and joins the results using Python. This method also supports the prefetching of `GenericRelation`  and `GenericForeignKey`.

***Cache Framework***

By caching queries, calculation results, or rendered content in an HTTP request, you will avoid expensive operations in the following requests. This translates into shorter response times and less processing on the server side. Django includes a robust cache system that allows you to cache data with different levels of granularity. You can cache a single query, the output of a specific view, parts of rendered template content, or your entire site. Items are stored in the cache system for a default time. You can specify the default timeout for cached data.

This is how you will usually use the cache framework when your application gets an HTTP request: 

1. Try to find the requested data in the cache
2. If found, return the cached data 
3.  If not found, perform the following steps: 

         ° Perform the query or processing required to obtain the data
         
         ° Save the generated data in the cache 
         
         ° Return the data

 Django comes with several cache backends.  These are the following:
 
 • backends.memcached.MemcachedCache or backends.memcached.     PyLibMCCache: A Memcached backend. Memcached is a fast and efficient memory-based cache server. The backend to use depends on the Memcached Python bindings you choose. 
 
 • backends.db.DatabaseCache: Use the database as a cache system.
 
• backends.filebased.FileBasedCache: Use the file storage system. This serializes and stores each cache value as a separate file.

 • backends.locmem.LocMemCache: A local memory cache backend. This the default cache backend. 
 
 • backends.dummy.DummyCache: A dummy cache backend intended only for development. It implements the cache interface without actually caching anything. 
 This cache is per-process and thread-safe.
 
***Monitoring Memcached***

In order to monitor Memcached, you will use a third-party package called django-memcache-status. This application displays statistics for your Memcached 
instances in the administration site. 
Install it with the following command:  

     pip install django-memcache-status

Django provides the following levels of caching, listed here by ascending order of granularity: 

• Low-level cache API: Provides the highest granularity. Allows you to cache specific queries or calculations. 

• Template cache: Allows you to cache template fragments. 

• Per-view cache: Provides caching for individual views. 

• Per-site cache: The highest-level cache. It caches your entire site.

Per-site cache is the highest-level cache. It allows you to cache your entire site. To allow the per-site cache, edit the settings.py file of your project 
and add the UpdateCacheMiddleware and FetchFromCacheMiddleware classes to the MIDDLEWARE setting, as follows:

    MIDDLEWARE = [   'django.middleware.security.SecurityMiddleware',   
    'django.contrib.sessions.middleware.SessionMiddleware',      'django.middleware.cache.UpdateCacheMiddleware',
     'django.middleware.common.CommonMiddleware',
     'django.middleware.cache.FetchFromCacheMiddleware',  ... ]

If the `USE_I18N` setting is set to True, the per-site middleware cache will respect the active language. If you use the `{% cache %}` template tag, 
you have to use one of the translation-specific variables available in templates to achieve the same result, such as `{% cache 600 name request.LANGUAGE_CODE %}`.
